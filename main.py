from flask import Flask, render_template, request, redirect, session
from s3_manager import upload_document
from s3_agent import process_s3_document
from chatbot import ask_document
from database import get_documents
from delete_document import delete_document
from bedrock_agent import ask_bedrock
from comparison_database import (
    save_comparison,
    get_comparisons,
    add_comparison_question
)
import os


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

UPLOAD_FOLDER = "uploads"


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


latest_result = None
latest_document_id = None



@app.route("/", methods=["GET", "POST"])
def home():

    global latest_result
    global latest_document_id


    result = latest_result
    answer = ""


    if "file" in request.files:

        file = request.files["file"]


        if file.filename:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )


            file.save(filepath)


            print("Uploading to S3...")


            filename = upload_document(filepath)


            print("Uploaded:", filename)


            latest_result = process_s3_document(filename)


            latest_document_id = filename


            result = latest_result



    if request.form.get("question"):

        question = request.form.get("question")


        if latest_document_id:

            answer = ask_document(
                question,
                latest_document_id
            )

        else:

            answer = "Please analyse a document first."



    documents = get_documents()


    return render_template(
        "index.html",
        result=result,
        answer=answer,
        documents=documents
    )




@app.route("/history")
def history():

    results = get_documents()

    return render_template(
        "history.html",
        results=results
    )




@app.route("/documents")
def documents():

    documents = get_documents()

    return render_template(
        "documents.html",
        documents=documents
    )




@app.route("/chat", methods=["GET", "POST"])
def chat():

    document_id = request.values.get(
        "document_id"
    )


    answer = ""


    if request.method == "POST":

        question = request.form.get(
            "question"
        )


        if question and document_id:

            answer = ask_document(
                question,
                document_id
            )

        else:

            answer = "Please select a document."



    return render_template(
        "chat.html",
        document_id=document_id,
        answer=answer
    )




@app.route("/delete/<document_id>")
def confirm_delete(document_id):

    return render_template(
        "delete.html",
        document_id=document_id
    )




@app.route("/delete/<document_id>", methods=["POST"])
def delete(document_id):

    print(
        "Deleting:",
        document_id
    )


    delete_document(document_id)


    return redirect("/documents")




@app.route("/compare", methods=["POST"])
def compare():

    selected_documents = request.form.getlist(
        "documents"
    )


    print(
        "Selected documents:",
        selected_documents
    )


    if len(selected_documents) < 2:

        return "Please select at least two documents to compare."



    documents = get_documents()


    selected_data = []


    for doc in documents:

        if doc["document_id"] in selected_documents:

            selected_data.append(doc)



    prompt = f"""

You are an intelligent document comparison assistant.

Compare these documents:

{selected_data}


Provide:

1. SUMMARY

2. SIMILARITIES

3. KEY DIFFERENCES

4. STRENGTHS

5. MISSING INFORMATION

6. RISKS OR CONCERNS

7. RECOMMENDATIONS


Give a professional comparison.

Finish with useful decision questions the user may ask.

"""


    comparison = ask_bedrock(prompt)


    comparison_id = save_comparison(
        selected_documents,
        comparison
    )


    session["comparison_id"] = comparison_id

    session["comparison"] = comparison

    session["qa_history"] = []


    return render_template(
        "compare.html",
        comparison=comparison,
        history=[]
    )



@app.route("/compare_question", methods=["POST"])
def compare_question():

    question = request.form.get(
        "question"
    )


    context = session.get(
        "comparison",
        ""
    )



    prompt = f"""

You are reviewing a previous document comparison.

Previous comparison:

{context}


User question:

{question}


Answer clearly.

Include:

- Direct answer
- Evidence from documents
- Missing information
- Risks or considerations

"""


    answer = ask_bedrock(prompt)



    comparison_id = session.get(
        "comparison_id"
    )


    if comparison_id:

        add_comparison_question(
            comparison_id,
            question,
            answer
        )



    history = session.get(
        "qa_history",
        []
    )


    history.append(
        {
            "question": question,
            "answer": answer
        }
    )


    session["qa_history"] = history



    return render_template(
        "compare.html",
        comparison=context,
        history=history
    )

@app.route("/comparison_history")
def comparison_history():

    comparisons = get_comparisons()


    return render_template(
        "comparison_history.html",
        comparisons=comparisons
    )

@app.route("/comparison/<comparison_id>")
def view_comparison(comparison_id):

    comparisons = get_comparisons()


    selected = None


    for item in comparisons:

        if item["comparison_id"] == comparison_id:

            selected = item
            break



    if not selected:

        return "Comparison not found"



    return render_template(
        "compare.html",
        comparison=selected["comparison"],
        history=[]
    )






if __name__ == "__main__":

    app.run(
        debug=True
    )