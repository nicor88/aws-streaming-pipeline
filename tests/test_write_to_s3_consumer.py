import consumers.write_to_s3.lambda_function as consumer

import pytest

@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv('STAGE', 'test')


def test_consumer():
    assert True
