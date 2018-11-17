import logging

import numpy

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    logger.info(event)
    output = {'numpy': numpy.__version__}
    return output
