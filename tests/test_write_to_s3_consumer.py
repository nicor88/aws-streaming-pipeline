import consumers.write_to_s3.lambda_function as consumer


def test_consumer():
    result = consumer.lambda_handler({}, None)
    assert result == {'numpy': '1.15.4'}
