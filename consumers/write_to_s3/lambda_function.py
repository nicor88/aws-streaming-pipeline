import base64
import datetime
import logging
import json
import uuid
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

s3 = boto3.client('s3')


def read_record(record):
    """
    Read Kinesis record as Python dictonary
    :param record:  dict, Kinesis record
    :return:
        dict
    """
    decoded_record = json.loads(base64.b64decode(record['kinesis']['data']).decode())
    # add
    decoded_record['event_id'] = record['kinesis']['sequenceNumber']
    return decoded_record


def read_records(kinesis_stream):
    """
    Read all the records in sent by Kinesis
    :param kinesis_input:
    :return:
        generator of records
    """
    records = kinesis_stream.get('Records')
    if not records:
        return []
    records_acc = (read_record(record) for record in records)
    return records_acc


def build_path(context_path, extension='json'):
    """
    Return an unique path used to write the batch to S3
    :param context_path: str, name of the context keyword used to write the batch to S3
    :param extension: str, by default is json
    :return:
        str
    """
    current_date = str(datetime.datetime.utcnow().date())
    formatted_timestamp = datetime.datetime.utcnow().strftime('%Y_%m_%d_%H')
    batch_id = str(uuid.uuid4())
    path = f'context={context_path}/date={current_date}/{formatted_timestamp}_{batch_id}.{extension}'
    return path


def write_to_s3(records):
    """
    Give a generator of records it write them to S3
    :param records: generator of records
    :return:
        dict, the s3 path were the events were written
    """
    bucket = os.environ['DESTINATION_S3_BUCKET']
    s3_key = build_path('write_to_s3', 'json')
    to_write = json.dumps(list(records))
    response = s3.put_object(Bucket=bucket,
                             Key=s3_key,
                             Body=to_write.encode())
    logger.info(response)
    s3_path = f's3://{bucket}/{s3_key}'
    return s3_path


def lambda_handler(event, context):
    logger.info(event)
    records = read_records(event)
    s3_path = write_to_s3(records)
    return {'s3_path': s3_path}
