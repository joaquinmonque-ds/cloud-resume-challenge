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
    Lambda entrypoint for incrementing the visitor count.
    Triggered by POST /put (API Gateway).
    """
    try:
        # Atomically increment "count" by 1 in DynamoDB
        response = table.update_item(
            Key={"ID": "visitor_count"},                 # Partition key
            UpdateExpression="ADD #count :inc",          # Increment by 1
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW"                   # Return the new value
        )

        # Extract new count from DynamoDB response
        new_count = int(response["Attributes"]["count"])

        # Return updated count in JSON format
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"count": new_count})
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
