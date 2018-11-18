import consumers.write_to_s3.lambda_function as consumer

import pytest


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


def test_consumer():
    assert True
