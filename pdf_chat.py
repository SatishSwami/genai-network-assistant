import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

load_dotenv()


def ask_pdf_question(
    vectorstore,
    question
):

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=os.getenv(
            "GOOGLE_API_KEY"
        )
    )

    prompt = f"""
You are an intelligent PDF assistant.

Use ONLY the provided context.

If the answer is not present,
say:

"The information is not available in the uploaded PDF."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "chunks": [
            doc.page_content
            for doc in docs
        ]
    }