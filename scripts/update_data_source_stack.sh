#!/bin/sh
set -e

STACK_NAME="data-sources"
TEMPLATE_URL="file://infrastructure/data-sources.yml"
STAGE="dev"

echo 'Checking template validity'
aws cloudformation validate-template --template-body $TEMPLATE_URL

echo 'Template valid, creating stack'
aws cloudformation update-stack --stack-name $STACK_NAME --template-body $TEMPLATE_URL --capabilities CAPABILITY_IAM \
	--parameters ParameterKey=Stage,ParameterValue=$STAGE

echo 'Waiting until stack update completes'
aws cloudformation wait stack-update-complete --stack-name $STACK_NAME

echo 'Stack updated successfully'
