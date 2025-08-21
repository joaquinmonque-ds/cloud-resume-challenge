# Minimal test for PutFunction.
# Uses moto to mock DynamoDB, seeds the item, and verifies it increments.

import json
import importlib
import pathlib
import sys

import boto3
from moto import mock_aws

TABLE_NAME = "cloud-resume-challenge"

def _add_lambda_path():
    """
    Make the put_function.py module importable whether running locally
    or in CI. Assumes this test file lives in cloud-resume-challenge/tests/.
    """
    here = pathlib.Path(__file__).resolve()
    project_dir = here.parents[1]  # .../cloud-resume-challenge/
    put_dir = project_dir / "put-function"
    path_str = str(put_dir)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

@mock_aws
def test_put_increments_count_ok():
    # Create mock table
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    ddb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # Seed starting count of 0
    ddb.put_item(
        TableName=TABLE_NAME,
        Item={"ID": {"S": "visitor_count"}, "count": {"N": "0"}},
    )

    # Import Lambda after table exists so boto3 resource binds fine
    _add_lambda_path()
    put_func = importlib.import_module("put_function")

    # Invoke handler
    resp = put_func.lambda_handler({}, {})
    assert resp["statusCode"] == 200

    # CORS present
    assert resp["headers"]["Access-Control-Allow-Origin"] == "*"

    # Body content should reflect incremented count
    body = json.loads(resp["body"])
    assert body["count"] == 1
