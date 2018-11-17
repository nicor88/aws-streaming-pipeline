import json
import uuid

import boto3

kinesis = boto3.client('kinesis')

STAGE = 'dev'

record = {'event_id': uuid.uuid4(), 'input': 'test'}
res = kinesis.put_record(StreamName=f'streaming-pipeline-{STAGE}-ingress-stream',
                         Data=json.dumps(record),
                         PartitionKey='event_id')

