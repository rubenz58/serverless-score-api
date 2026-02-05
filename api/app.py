import os
import json
import boto3
from datetime import datetime
from decimal import Decimal
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["SCORES_TABLE"])
print("TABLE NAME:", os.environ.get("SCORES_TABLE"))
print("AWS REGION:", boto3.session.Session().region_name)

# import requests

def handler(event, context):
    method = event["httpMethod"]
    path_params = event.get("pathParameters") or {}

    if method == "GET" and path_params.get("id"):
        return get_score(event)
    
    if method == "POST" and event["path"] == "/score":
        return post_score(event)
    
    return {
        "statusCode": 404,
        "body": "Not found"
    }

def get_score(event):

    path_params = event.get("pathParameters") or {}
    score_id = path_params.get("id")

    if not score_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing score id",
            }),
        }
    
    response = table.get_item(
        Key={"id": score_id}
    )

    item = response.get("Item")
    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Score not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(serialize_dynamodb_item(item))
    }

def post_score(event):
    body = json.loads(event.get("body", "{}"))
    score_id = str(uuid.uuid4())
    print(score_id)
    value = body.get("value")

    if value is None:
        return {"statusCode": 400, "body": "Missing value"}
    
    table.put_item(
        Item={
            "id": score_id,
            "value": value,
            "created_at": datetime.utcnow().isoformat()
        }
    )

    return {
        "statusCode": 201,
        "body": json.dumps({"id": score_id})
    }


def serialize_dynamodb_item(item):
    def convert(value):
        if isinstance(value, Decimal):
            return int(value)
        return value

    return {k: convert(v) for k, v in item.items()}