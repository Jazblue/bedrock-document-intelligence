import boto3
from datetime import datetime
import uuid


print(
    "AWS Region:",
    boto3.Session().region_name
)


dynamodb = boto3.resource(
    "dynamodb"
)


table = dynamodb.Table(
    "document_comparisons"
)



def save_comparison(
    documents,
    comparison
):

    comparison_id = str(
        uuid.uuid4()
    )


    table.put_item(

        Item={

            "comparison_id": comparison_id,

            "documents": documents,

            "comparison": comparison,

            "created": datetime.now().isoformat(),

            "questions": []

        }

    )


    print(
        "Saved comparison:",
        comparison_id
    )


    return comparison_id




def get_comparisons():


    response = table.scan()


    return response.get(
        "Items",
        []
    )




def add_comparison_question(
    comparison_id,
    question,
    answer
):

    response = table.get_item(

        Key={
            "comparison_id": comparison_id
        }

    )


    item = response.get(
        "Item"
    )


    if not item:

        print(
            "Comparison not found:",
            comparison_id
        )

        return



    questions = item.get(
        "questions",
        []
    )


    questions.append(

        {
            "question": question,
            "answer": answer
        }

    )



    result = table.update_item(

        Key={

            "comparison_id": comparison_id

        },


        UpdateExpression=
        "SET questions = :q",


        ExpressionAttributeValues={

            ":q": questions

        },


        ReturnValues="ALL_NEW"

    )


    print(
        "Saved comparison question"
    )


    print(
        result["Attributes"]
    )