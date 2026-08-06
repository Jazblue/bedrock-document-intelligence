import boto3
from dotenv import load_dotenv
from bedrock_agent import ask_bedrock

load_dotenv()


TABLE_NAME = "document-analysis-results"


dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)



def get_document(document_id):

    print("Looking for document:", document_id)


    if not document_id:

        return None


    response = table.get_item(
        Key={
            "document_id": document_id
        }
    )


    return response.get("Item")



def ask_document(question, document_id):


    document = get_document(document_id)


    if not document:

        return "Document not found."



    prompt = f"""
You are an intelligent document assistant.

You must answer using only the document analysis provided.

Document name:
{document.get('document_name')}


Document type:
{document.get('document_type')}


Analysis:
{document.get('result')}


User question:
{question}


Give a clear and concise answer.
"""


    answer = ask_bedrock(prompt)


    return answer