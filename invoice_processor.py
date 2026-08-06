from bedrock_agent import ask_bedrock
import json


def process_invoice(text):

    prompt = f"""
You are an invoice extraction assistant.

Extract the invoice information from this text.

Return ONLY valid JSON.

Required fields:
- invoice_number
- supplier
- customer
- line_items
- total

Document:

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
        "document_type": "invoice",
        "action": "extract_invoice_details",
        "data": data
    }