from bedrock_agent import ask_bedrock
import json


def classify_document(text):

    prompt = f"""
You are a document classification agent.

Classify this document into exactly one category:

invoice
contract
general

Return ONLY JSON:

{{
    "document_type": "contract"
}}

Document:

{text[:4000]}
"""

    response = ask_bedrock(prompt)

    try:
        clean = response.replace("```json", "").replace("```", "").strip()

        result = json.loads(clean)

        return result["document_type"]

    except Exception:
        return "general"