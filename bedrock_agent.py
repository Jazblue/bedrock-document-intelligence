import boto3
import os
import json
from dotenv import load_dotenv
from logger import logger


load_dotenv()


bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv(
        "AWS_REGION",
        "us-east-1"
    )
)


def ask_bedrock(prompt):

    logger.info(
        "Bedrock request started"
    )


    try:

        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 2000,
                "temperature": 0.2
            }
        }


        response = bedrock.invoke_model(
            modelId=os.getenv(
                "BEDROCK_MODEL_ID",
                "amazon.nova-lite-v1:0"
            ),
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )


        result = json.loads(
            response["body"].read()
        )


        logger.info(
            "Bedrock request completed successfully"
        )


        return result[
            "output"
        ][
            "message"
        ][
            "content"
        ][0]["text"]


    except Exception as error:

        logger.error(
            f"Bedrock request failed: {error}"
        )


        return (
            "Bedrock processing failed. "
            "Please try again later."
        )