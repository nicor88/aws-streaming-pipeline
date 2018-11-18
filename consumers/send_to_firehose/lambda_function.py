import asyncio
import base64
import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

firehose = boto3.client('firehose')


def read_record(record):
    """
    Read Kinesis record as Python dictonary
    :param record:  dict, Kinesis record
    :return:
        dict
    """
    decoded_record = json.loads(base64.b64decode(record['kinesis']['data']).decode())
    decoded_record['event_id'] = record['kinesis']['sequenceNumber']
    return decoded_record


def read_records(kinesis_stream):
    """
    Read all the records in sent by Kinesis
    :param kinesis_stream: dict, input coming from kinesis stream
    :return:
        generator of records
    """
    records = kinesis_stream.get('Records')
    if not records:
        return []
    records_acc = (read_record(record) for record in records)
    return records_acc


def send_record(record):
    firehose_delivery_stream = os.environ['FIREHOSE_DELIVERY_STREAM']
    record_with_separator = str(record) + '\n'
    record_for_firehose = {'Data': record_with_separator.encode()}
    response = firehose.put_record(DeliveryStreamName=firehose_delivery_stream,
                                   Record=record_for_firehose)
    return response


async def async_sender(records):
    """
    Send records in an asynchronous to speed up the sending process
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


def lambda_handler(event, context):
    logger.info(event)

    records = read_records(event)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(
        async_sender(records=records)
    )
    success_sending = (res for res in results if res['ResponseMetadata']['HTTPStatusCode'] == 200)
    result = f'{len(list(success_sending))} records were sent successfully'
    logger.info(result)
    return {'result': result}
