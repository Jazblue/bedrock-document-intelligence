import boto3
from dotenv import load_dotenv

load_dotenv()

TABLE_NAME = "document-analysis-results"

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)


def get_documents():

    response = table.scan()

    items = response.get("Items", [])

    documents = []

    for item in items:
        documents.append(
            item["document_id"]
        )

    return documents