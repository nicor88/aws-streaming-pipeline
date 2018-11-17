[![Build Status](https://travis-ci.org/nicor88/aws-streaming-pipeline.svg?branch=master)](https://travis-ci.org/nicor88/aws-streaming-pipeline)

# aws-streaming-pipeline

## Infrastructure
bash scripts/created_data_source_stack.sh

cd ../consumers/init_consumer 
zip -r init.zip .
aws s3 cp init.zip s3://streaming-pipeline-dev-deployment/consumers/
aws s3 cp consumers/init_consumer/init.zip s3://streaming-pipeline-dev-deployment/consumers/ 
 
## Producer
It's possible to send some samples records just calling:
<pre>
python producer/producer.py
</pre>

## Consumers


## Unit tests
<pre>
pytest -vv tests/*
</pre>