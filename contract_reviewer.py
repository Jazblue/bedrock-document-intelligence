from bedrock_agent import ask_bedrock
import json


def review_contract(text):

    prompt = f"""
You are a contract analysis assistant.

Review this contract and return ONLY valid JSON.

Extract:

- parties
- contract purpose
- payment terms
- termination terms
- liability terms
- governing law
- risks
- recommendations

Contract text:

{text}
"""

    response = ask_bedrock(prompt)

    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

    except Exception:
        data = {
            "raw_response": response
        }

    return {
        "document_type": "contract",
        "action": "contract_review",
        "data": data
    }