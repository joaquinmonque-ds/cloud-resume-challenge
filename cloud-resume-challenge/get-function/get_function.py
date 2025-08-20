import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource and reference the table
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cloud-resume-challenge")

# Reusable CORS headers (must be returned in every response for browser access)
HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
}

def lambda_handler(event, context):
    """
    Lambda entrypoint for fetching the current visitor count.
    Triggered by GET /get (API Gateway).
    """
    try:
        # Attempt to read the visitor_count item from DynamoDB
        response = table.get_item(Key={"ID": "visitor_count"})

        # If the item doesn't exist, return 404
        if "Item" not in response:
            return {
                "statusCode": 404,
                "headers": HEADERS,
                "body": json.dumps({"error": "Item not found"})
            }

        # Extract count value (convert from Decimal to int)
        count = int(response["Item"]["count"])

        # Return count in JSON format
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"count": count})
        }

    except ClientError as e:
        # AWS service error (e.g., DynamoDB issue)
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": e.response['Error']['Message']})
        }
    except Exception as e:
        # Generic error catch-all
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
