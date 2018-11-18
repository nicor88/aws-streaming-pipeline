import asyncio
import csv
import json
import logging
import uuid

import boto3

STAGE = 'dev'
STREAM = f'streaming-pipeline-{STAGE}-ingress-stream'
BASE_INPUT_PATH = 'producer/sample.csv'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

kinesis = boto3.client('kinesis')


def read_csv(file_path):
    """
    Read a CSV and returns a generator of dictionaries
    :param file_path: str, file path where the csv is located
    :return:

    """
    buffer = csv.DictReader(open(file_path))
    csv_as_list = (dict(el) for el in list(buffer))
    return csv_as_list


def send_record(record):
    record_to_send = {'event_id': str(uuid.uuid4())}
    record_to_send.update(record)
    res = kinesis.put_record(StreamName=STREAM,
                             Data=json.dumps(record),
                             PartitionKey='event_id')
    logger.info(res)
    return res


async def async_sender(records):
    """
    Send records in an asynchronous way to speed up the sending process
    :param records: list of dictionaries
    :return:
        list, responses of the sending process
    """
    data = []
    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, send_record, record)
               for record in records]
    for response in await asyncio.gather(*futures):
        data.append(response)
    return data


def read_and_send():
    records_to_send = read_csv(BASE_INPUT_PATH)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(
        async_sender(records=records_to_send)
    )
    return results


if __name__ == '__main__':
    logger.info('ready to send')
    sending_result = read_and_send()
    success_sending = (res for res in sending_result if res['ResponseMetadata']['HTTPStatusCode'] == 200)
    logger.info(f'{len(list(success_sending))} records were sent successfully')
