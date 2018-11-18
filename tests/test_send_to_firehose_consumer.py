import consumers.send_to_firehose.lambda_function as consumer

import pytest
from unittest.mock import Mock


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv('STAGE', 'test')


@pytest.fixture
def kinesis_records():
    kinesis_records = {'Records': [
        {
            'kinesis': {
                'kinesisSchemaVersion': '1.0',
                'partitionKey': 'event_id',
                'sequenceNumber': '49590221985993876996108612573478580168307040747492737026',
                'data': 'eyJUUklQX0lEIjogIlQxNyIsICJDQUxMX1RZUEUiOiAiQyIsICJPUklHSU5fQ0FMTCI6ICJOQSIsICJPUklHSU5fU1RBTkQiOiAiTkEiLCAiVEFYSV9JRCI6ICIyMDAwMDQ2NyIsICJUSU1FU1RBTVAiOiAiMTQwODAzODgwNCIsICJEQVlfVFlQRSI6ICJBIiwgIk1JU1NJTkdfREFUQSI6ICJGYWxzZSIsICJQT0xZTElORSI6ICJbWy04LjYyNzA5NCw0MS4xNjY5MzZdLFstOC42MjcwNDksNDEuMTY2OV0sWy04LjYyNjY0NCw0MS4xNjY5XSxbLTguNjI2NjI2LDQxLjE2NjkwOV0sWy04LjYyNjYxNyw0MS4xNjY5MDldLFstOC42MjY2MTcsNDEuMTY2OV0sWy04LjYyNjYwOCw0MS4xNjY5XSxbLTguNjI2NTk5LDQxLjE2Njg5MV0sWy04LjYyNjkyMyw0MS4xNjY1MDRdLFstOC42MjgwNzUsNDEuMTY2MTM1XSxbLTguNjI5NDYxLDQxLjE2NTU3N10sWy04LjYzMDgwMiw0MS4xNjUwMTldLFstOC42MzI1NDgsNDEuMTY0MTU1XSxbLTguNjMzNTM4LDQxLjE2MzM0NV0sWy04LjYzMjc2NCw0MS4xNjIyOTJdLFstOC42MzE5NDUsNDEuMTYxMjQ4XSxbLTguNjMwNjA0LDQxLjE1OTQ5M10sWy04LjYzMDM0Myw0MS4xNTg5MDhdLFstOC42MzA0MDYsNDEuMTU4ODU0XSxbLTguNjMwMjE3LDQxLjE1ODYyOV0sWy04LjYzMDMyNSw0MS4xNTgzMDVdLFstOC42MzA0NTEsNDEuMTU3NTY3XSxbLTguNjI5NTQyLDQxLjE1Njg4M10sWy04LjYyOTczMSw0MS4xNTU3MzFdLFstOC42MjkyMTgsNDEuMTU1MTI4XSxbLTguNjI5MDc0LDQxLjE1NTE0Nl0sWy04LjYyOTA2NSw0MS4xNTUxMzddXSJ9',
                'approximateArrivalTimestamp': 1542472236.14
            },
            'eventSource': 'aws:kinesis',
            'eventVersion': '1.0',
            'eventID': 'shardId-000000000000:49590221985993876996108612573478580168307040747492737026',
            'eventName': 'aws:kinesis:record',
            'invokeIdentityArn': 'arn:aws:iam::749785218022:role/stream-dev-WriteToS3ConsumerExecutionRole-7LAMYIDWU7G0',
            'awsRegion': 'us-east-1',
            'eventSourceARN': 'arn:aws:kinesis:us-east-1:749785218022:stream/streaming-pipeline-dev-ingress-stream'
        },
        {
            'kinesis': {
                'kinesisSchemaVersion': '1.0',
                'partitionKey': 'event_id',
                'sequenceNumber': '49590221985993876996108612573479789094126655445386919938',
                'data': 'eyJUUklQX0lEIjogIlQxMiIsICJDQUxMX1RZUEUiOiAiQyIsICJPUklHSU5fQ0FMTCI6ICJOQSIsICJPUklHSU5fU1RBTkQiOiAiTkEiLCAiVEFYSV9JRCI6ICIyMDAwMDE2MCIsICJUSU1FU1RBTVAiOiAiMTQwODAzODk0NiIsICJEQVlfVFlQRSI6ICJBIiwgIk1JU1NJTkdfREFUQSI6ICJGYWxzZSIsICJQT0xZTElORSI6ICJbWy04LjU4NTY5NCw0MS4xNDg2MDNdLFstOC41ODU3NTcsNDEuMTQ4Njg0XSxbLTguNTg1NzEyLDQxLjE0ODg4Ml0sWy04LjU4NTc1Nyw0MS4xNDg5NjNdLFstOC41ODU4MzgsNDEuMTQ4OTU0XSxbLTguNTg2MDYzLDQxLjE0ODk3Ml0sWy04LjU4NjE3MSw0MS4xNDg5NzJdLFstOC41ODczMjMsNDEuMTQ5MTUyXSxbLTguNTg4MDA3LDQxLjE0OTM4Nl0sWy04LjU4ODczNiw0MS4xNDk2MDJdLFstOC41OTEwMzEsNDEuMTUwMTg3XSxbLTguNTkyMTY1LDQxLjE1MDQ4NF0sWy04LjU5MjIwMSw0MS4xNTA0OTNdLFstOC41OTMzODksNDEuMTUwODQ0XSxbLTguNTk0NTUsNDEuMTUwNjY0XSxbLTguNTk1OTE4LDQxLjE0OTg3Ml0sWy04LjU5NjY0Nyw0MS4xNDk0MzFdXSJ9',
                'approximateArrivalTimestamp': 1542472236.163
            },
            'eventSource': 'aws:kinesis',
            'eventVersion': '1.0',
            'eventID': 'shardId-000000000000:49590221985993876996108612573479789094126655445386919938',
            'eventName': 'aws:kinesis:record',
            'invokeIdentityArn': 'arn:aws:iam::749785218022:role/stream-dev-WriteToS3ConsumerExecutionRole-7LAMYIDWU7G0',
            'awsRegion': 'us-east-1',
            'eventSourceARN': 'arn:aws:kinesis:us-east-1:749785218022:stream/streaming-pipeline-dev-ingress-stream'
        },
    ]}
    return kinesis_records


@pytest.fixture
def firehose_response():
    return {
        'RecordId': 'oUcx4VzAGhBMBv0F5JppNkzL3NNMyvJtwXrk2AqWM9qVHU/Ugb2nhQIFEGxxM/UF0aEehznzygrUa0ctwNliC3zYu0YMsfM0aDEh1pVlJdLGKIklGe39KEbMu2FNnpY17M95q7rJvCAzyN8jmqcSWWk09ry6f2jdIgFeMb06oCNi43tugJ4APAkmNWJg4h2bEaruMYLrkvf7hEjbMGNNtcNZEgeWgpQD',
        'Encrypted': False,
        'ResponseMetadata': {'RequestId': 'c9efce37-32ea-a50c-9d84-2c90c2274435', 'HTTPStatusCode': 200,
                             'HTTPHeaders': {'x-amzn-requestid': 'c9efce37-32ea-a50c-9d84-2c90c2274435',
                                             'x-amz-id-2': '3MCFERUklelD53rMot9T504NU/nleF9V3G3pPgw5Xp4NWlhvsMilIoyl71qBj01WAtSlQp2EpQi9JftW51QI7WSjFwC+Tw2i',
                                             'content-type': 'application/x-amz-json-1.1', 'content-length': '257',
                                             'date': 'Sun, 18 Nov 2018 21:57:59 GMT'}, 'RetryAttempts': 0}}


def test_read_record(kinesis_records):
    record = kinesis_records['Records'][0]
    decoded_record = consumer.read_record(record)
    assert isinstance(decoded_record, dict)
    assert 'event_id' in decoded_record.keys()


def test_read_records(kinesis_records):
    decoded_records = consumer.read_records(kinesis_records)
    assert len(list(decoded_records)) == 2


def test_read_records_with_empty_input():
    decoded_records = consumer.read_records({})
    assert decoded_records == []


def test_lambda_function(monkeypatch, kinesis_records, firehose_response):
    def mock_send_record(record):
        assert isinstance(record, dict)
        return firehose_response

    monkeypatch.setattr('consumers.send_to_firehose.lambda_function.send_record', mock_send_record)

    result = consumer.lambda_handler(kinesis_records, None)
    assert result.get('result') == '2 records were sent successfully'
