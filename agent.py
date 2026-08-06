from pdf_reader import read_pdf
from document_classifier import classify_document
from invoice_processor import process_invoice
from contract_reviewer import review_contract
from bedrock_agent import ask_bedrock
from document_chunker import chunk_text
import glob
import os


def process_document(file_path):

    # Allow wildcard paths like documents/ACFr*.pdf
    if "*" in file_path:

        matches = glob.glob(file_path)

        if not matches:
            raise FileNotFoundError(
                f"No files found matching: {file_path}"
            )

        file_path = matches[0]


    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )


    print(f"Processing: {file_path}")


    # Extract PDF text
    text = read_pdf(file_path)


    if not text.strip():

        return {
            "error": "No readable text found in PDF"
        }


    # Decide document type
    document_type = classify_document(text)


    print(f"Detected document type: {document_type}")


    # Specialist agents

    if document_type == "invoice":

        return process_invoice(text)



    elif document_type == "contract":

        return review_contract(text)



    else:

        chunks = chunk_text(text)

        chunk_results = []


        for index, chunk in enumerate(chunks):

            print(
                f"Analysing chunk {index + 1} of {len(chunks)}"
            )


            response = ask_bedrock(
                f"""
You are an intelligent document analysis system.

Analyse this section of a document.

Identify:

- Important information
- Dates
- People or organisations
- Skills
- Experience
- Risks
- Missing information


Document section:

{chunk}

"""
            )


            chunk_results.append(response)



        combined_response = "\n\n".join(
            chunk_results
        )



        final_summary = ask_bedrock(
    f"""
You are a senior document reviewer and recruitment analyst.

Using the analysis from the document sections below,
create one final structured professional profile report.

Use this format:

DOCUMENT TYPE:

SUMMARY:

SUITABILITY SCORE:
Give an estimated suitability percentage for common professional roles.

MATCHING ROLES:
List roles this person may be suitable for.

KEY STRENGTHS FOR EMPLOYERS:
List the strongest skills, experience, and qualifications.

KEY INFORMATION:

EXPERIENCE:

SKILLS:

EDUCATION OR QUALIFICATIONS:

DATES:

PEOPLE OR ORGANISATIONS:

RISKS OR ISSUES:
Identify missing information, concerns, or areas requiring verification.

AREAS TO IMPROVE:
Suggest skills, certifications, or experience that would strengthen the profile.

RECOMMENDED ACTIONS:
Provide practical next steps.


Document analysis sections:

{combined_response}

"""
)



        return {
            "document_type": "general",
            "action": "bedrock_analysis",
            "data": final_summary
        }