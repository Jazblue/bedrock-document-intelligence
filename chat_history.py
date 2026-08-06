import boto3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


TABLE_NAME = "document-chat-history"


dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)



def save_chat(document_id, question, answer):

    item = {

        "document_id": document_id,

        "timestamp": datetime.now().isoformat(),

        "question": question,

        "answer": answer

    }


    table.put_item(
        Item=item
    )


    print("Chat history saved")




def get_chat_history(document_id):

    response = table.query(

        KeyConditionExpression=
        "document_id = :doc",

        ExpressionAttributeValues={

            ":doc": document_id

        }

    )


    return response.get("Items", [])