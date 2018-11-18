#!/bin/sh
set -e

STAGE="dev"
STACK_NAME="data-sources-$STAGE"
TEMPLATE_URL="file://infrastructure/data-sources.yml"


echo 'Checking template validity'
aws cloudformation validate-template --template-body $TEMPLATE_URL

echo 'Template valid, creating stack'
aws cloudformation create-stack --stack-name $STACK_NAME --template-body $TEMPLATE_URL --capabilities CAPABILITY_IAM \
	--parameters ParameterKey=Stage,ParameterValue=$STAGE

echo 'Waiting until stack create completes'
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME

echo 'Stack created successfully'
