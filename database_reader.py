import boto3
from dotenv import load_dotenv

load_dotenv()

TABLE_NAME = "document-analysis-results"

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)


def get_latest_document():

    response = table.scan()

    items = response.get("Items", [])

    if not items:
        return None

    latest = sorted(
        items,
        key=lambda x: x["processed_time"],
        reverse=True
    )[0]

    return latest