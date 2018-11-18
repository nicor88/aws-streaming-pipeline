[![Build Status](https://travis-ci.org/nicor88/aws-streaming-pipeline.svg?branch=master)](https://travis-ci.org/nicor88/aws-streaming-pipeline)

# aws-streaming-pipeline

## Requirements
* python3.6
* pip
* Docker

### Development
Install the libs running:
<pre>
pip install -r requirements.txt
for i in consumers/*/; do pip install -r $i"requirements.txt"; done
</pre>

## Infrastructure
The infrastructure is provisioned using Cloudformation. It is split in 2 mains stacks:
* data-sources stack that consists of:
	* S3 Bucket used for to store the artifacts produced to deploy the Lambda functions
	* S3 Bucket used to store the Output of the Lambda functions

* stream stack that consists of:
	* Kinesis stream with 2 shards
	* Lambda function *write_to_s3*, setup as consumer for the stream, to write the events to S3
	* Execution role for the Lambda function *write_to_s3*
	* Lambda function *send_to_firehose*, setup as consumer for the stream, to send the event to Firehose Delivery Stream
	* Execution role for the Lambda function *send_to_firehose*
	* Firehose Delivery Stream, configured to deliver to S3
	* Firehose Delivery Stream Execution Role, necessary to put object to S3

### Init the infrastructure
* First create the `data-sources` stack
	<pre>
	bash scripts/create_data_source_stack.sh
	</pre>

* Create a zipped file to init the lambda functions, and upload to S3
	<pre>
	cd consumers/init_consumer
	zip -r init.zip .
	aws s3 cp init.zip s3://streaming-pipeline-dev-deployment/consumers/
	cd ..
	</pre>
	
* Create the `stream` stack
	<pre>
	bash scripts/create_stream_stack.sh
	</pre>
	**NOTE**: if the S3 key consumers/init.zip is not uploaded in the S3 Bucket used for deployment, the stack creation will fail

All the stack and resources contains a stage parameters, to simplify the creation of the stacks for multiple stages.
 
### Producer
In order to test the proposed solution, we needed to implement a producer, that put the records to the stream.
The producer use a sample csv from a []Kaggle competition](https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i/data)
It's possible to the sample records, just calling:
<pre>
python producer/producer.py
</pre>

## Unit tests
<pre>
pytest -vv tests/*
</pre>

## CI/CD
At each push Travis is triggered. It will take care of:
* running the unit tests
* preparing the zipped lambda function(containing all needed requirements)
* update the stream stack with the update version of the lambdas

## Improvements and Considerations
2 consumers for Kinesis stream were created. Write to S3 consumer receive the records and write them as JSON to S3.
The file written by such consumer can be really small, the size can be even smaller when adding more shards.
This is due to the fact that the lambda is invoked many time, with a limited amount of events.
The produced files are hard to read with applications like Spark/Presto/Athena, because they will create a not needed network overhead.
To solve this problem we can easily create a consumer that send the record to Firehose, then firehose will take care of
writing the file to S3, when specific conditions are reached, for example in this implementations
the files saved written to S3 with a max size of 5MB. In this specific implementation, each JSON is one line of the file.
Such format, called JSONlines will make the file easier to be read by Spark/Presto/Athena.
To test that, we can easily create an Athen Table using the DDL inside the folder `Athena`.
