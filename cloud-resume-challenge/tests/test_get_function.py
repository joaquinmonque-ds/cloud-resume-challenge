# Minimal “does it return JSON & statusCode 200 when item exists” test.
# We mock DynamoDB with moto and seed the item.

import json
import importlib
from moto import mock_aws
import boto3

TABLE_NAME = "cloud-resume-challenge"

@mock_aws
def test_get_returns_count_ok(monkeypatch):
    # Create table
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    ddb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    # Seed item
    ddb.put_item(
        TableName=TABLE_NAME,
        Item={"ID": {"S": "visitor_count"}, "count": {"N": "42"}}
    )

    # Import the lambda after table exists so boto3 resource binds fine
    get_func = importlib.import_module("get_function")  # module in get-function/

    resp = get_func.lambda_handler({}, {})
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["count"] == 42
    # CORS present?
    assert resp["headers"]["Access-Control-Allow-Origin"] == "*"
