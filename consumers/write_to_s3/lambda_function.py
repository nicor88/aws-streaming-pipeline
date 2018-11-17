import base64
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def read_and_validate(record):
    decoded_record = json.loads(base64.b64decode(record['kinesis']['data']).decode())
    decoded_record['sequenceNumber'] = record['kinesis']['sequenceNumber']
    return decoded_record


def read_records(records):
    if not records:
        return []
    records_acc = (read_and_validate(record) for record in records)
    return records_acc


def lambda_handler(event, context):
    logger.info(event)
    output = {'output': 'hello world'}
    records = event.get('Records')
    valid_records = read_records(records)
    logger.info(f'{len(list(valid_records))} records were read correctly')
    # TODO write records to S3
    return output
