import boto3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


TABLE_NAME = "document-analysis-results"


dynamodb = boto3.resource(
    "dynamodb"
)


table = dynamodb.Table(
    TABLE_NAME
)


def start_processing(document_id):

    item = {

        "document_id": document_id,

        "document_name": document_id,

        "processed_time": datetime.now().isoformat(),

        "status": "PROCESSING"

    }


    table.put_item(
        Item=item
    )


    print(
        f"Document status: PROCESSING - {document_id}"
    )


def mark_failed(
    document_id,
    error_message
):

    table.update_item(

        Key={

            "document_id": document_id

        },

        UpdateExpression="""
            SET #status = :status,
                error_message = :error
        """,

        ExpressionAttributeNames={

            "#status": "status"

        },

        ExpressionAttributeValues={

            ":status": "FAILED",

            ":error": str(error_message)

        }

    )


    print(
        f"Document status: FAILED - {document_id}"
    )


def save_result(
    document_id,
    result
):

    item = {

        "document_id": document_id,

        "document_name": document_id,

        "processed_time": datetime.now().isoformat(),

        "status": "COMPLETED",

        "document_type": result.get(
            "document_type"
        ),

        "action": result.get(
            "action"
        ),

        "result": str(result)

    }


    table.put_item(
        Item=item
    )


    print(
        "Saved result to DynamoDB"
    )


def get_documents():

    response = table.scan()

    return response.get(
        "Items",
        []
    )