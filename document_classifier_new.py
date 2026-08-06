def classify_document(text):

    text_lower = text.lower()


    contract_keywords = [
        "agreement",
        "contract",
        "terms and conditions",
        "termination",
        "governing law",
        "liability",
        "intellectual property",
        "confidentiality"
    ]


    invoice_keywords = [
        "invoice",
        "invoice number",
        "bill to",
        "amount due",
        "total:",
        "payment due"
    ]


    contract_score = sum(
        1 for word in contract_keywords
        if word in text_lower
    )


    invoice_score = sum(
        1 for word in invoice_keywords
        if word in text_lower
    )


    if contract_score > invoice_score:
        return "contract"


    elif invoice_score > contract_score:
        return "invoice"


    else:
        return "general"