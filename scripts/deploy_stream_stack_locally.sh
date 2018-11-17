#!/bin/sh
set -e

STAGE="dev"
STACK_NAME="stream-$STAGE"
TEMPLATE_URL="file://infrastructure/stream.yml"
UUID=$(openssl rand -base64 10)
S3_DEPLOYMENT_BUCKET="s3://streaming-pipeline-$STAGE-deployment"
BASE_CONSUMER_PATH=consumers
BASE_S3_KEY=$BASE_CONSUMER_PATH/$UUID
BASE_S3_PATH=$S3_DEPLOYMENT_BUCKET/$BASE_S3_KEY

CONSUMERS=(write_to_s3 send_to_firehose)
for i in ${CONSUMERS[*]}; do
	echo "Building $i";
	CONSUMER_NAME=$i
	CONSUMER_PATH=$BASE_CONSUMER_PATH/$CONSUMER_NAME
	rm -rf $CONSUMER_PATH/.build
	mkdir -p $CONSUMER_PATH/.build
	cp $CONSUMER_PATH/*.py $CONSUMER_PATH/.build

	# install libs locally as it was a linux environment
	docker run --rm -v `pwd`:/var/task:z lambci/lambda:build-python3.6 python3.6 -m pip --isolated install -t $CONSUMER_PATH/.build -r $CONSUMER_PATH/requirements.txt

	cd $CONSUMER_PATH/.build
	zip -r $CONSUMER_NAME.zip .
	aws s3 cp $CONSUMER_NAME.zip $BASE_S3_PATH/$CONSUMER_NAME.zip
	DEPLOYMENT_KEY=$BASE_S3_KEY/$CONSUMER_NAME.zip
	echo "$CONSUMER_NAME.zip uploaded to $DEPLOYMENT_KEY"
	cd ../../..
done

WRITE_TO_S3_DEPLOYMENT_KEY=$BASE_S3_KEY/${CONSUMERS[0]}.zip
SEND_TO_FIREHOSE_KEY=$BASE_S3_KEY/${CONSUMERS[1]}.zip

# update cfn stack
echo 'Checking template validity'
aws cloudformation validate-template --template-body $TEMPLATE_URL

echo 'Template valid, creating stack'
aws cloudformation update-stack --stack-name $STACK_NAME --template-body $TEMPLATE_URL --capabilities CAPABILITY_IAM \
	--parameters ParameterKey=Stage,ParameterValue=$STAGE ParameterKey=S3KeyWriteToS3Consumer,ParameterValue=$WRITE_TO_S3_DEPLOYMENT_KEY \
		ParameterKey=S3KeySendToFirehoseConsumer,ParameterValue=$SEND_TO_FIREHOSE_KEY

echo 'Waiting until stack create completes'
aws cloudformation wait stack-update-complete --stack-name $STACK_NAME

echo 'Stack created successfully'
