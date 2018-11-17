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


def read_and_validate(record):
    decoded_record = json.loads(base64.b64decode(record['kinesis']['data']).decode())
    decoded_record['sequenceNumber'] = record['kinesis']['sequenceNumber']
    return decoded_record


def read_records(records):
    if not records:
        return []
    records_acc = (read_and_validate(record) for record in records)
    return records_acc


def build_path(base_path, extension='json'):
    current_date = str(datetime.datetime.utcnow().date())
    formatted_timestamp = datetime.datetime.utcnow().strftime('%Y_%m_%d_%H')
    batch_id = str(uuid.uuid4())
    path = f'context={base_path}/date={current_date}/{formatted_timestamp}_{batch_id}.{extension}'
    return path


def write_to_s3(records):
    bucket = os.environ['DESTINATION_S3_BUCKET']
    s3_key = build_path('writ_to_s3', 'json')
    to_write = json.dumps(records)
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
