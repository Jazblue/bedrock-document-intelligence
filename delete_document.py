import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = "bedrock-document-agent-storage"

s3 = boto3.client("s3")

dynamodb = boto3.resource("dynamodb")

analysis_table = dynamodb.Table("document-analysis-results")
chat_table = dynamodb.Table("document-chat-history")


def delete_document(document_id):

    # Delete PDF from S3
    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=document_id
    )

    # Delete analysis record
    analysis_table.delete_item(
        Key={
            "document_id": document_id
        }
    )

    # Delete chat history
    response = chat_table.query(
        KeyConditionExpression=Key("document_id").eq(document_id)
    )

    for item in response.get("Items", []):

        chat_table.delete_item(
            Key={
                "document_id": item["document_id"],
                "timestamp": item["timestamp"]
            }
        )

    print(f"{document_id} deleted successfully.")