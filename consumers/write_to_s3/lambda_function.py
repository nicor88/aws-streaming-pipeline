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


def read_records(records):
    """
    Read all the records in sent by Kinesis
    :param records:
    :return:
        generator of records
    """
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
        dict, answer from boto3 put operation
    """
    bucket = os.environ['DESTINATION_S3_BUCKET']
    s3_key = build_path('write_to_s3', 'json')
    to_write = json.dumps(list(records))
    response = s3.put_object(Bucket=bucket,
                             Key=s3_key,
                             Body=to_write.encode())
    return response


def lambda_handler(event, context):
    logger.info(event)
    records = event.get('Records')
    valid_records = read_records(records)
    response = write_to_s3(valid_records)
    logger.info(response)
    return {'output': 'records were written successfully'}
