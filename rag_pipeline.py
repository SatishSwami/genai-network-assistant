import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def load_rag_pipeline():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
 )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    return retriever, llm


def get_answer(question):

    retriever, llm = load_rag_pipeline()

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an expert Cisco Network Troubleshooting Assistant.

Rules:
1. Use only the provided context.
2. If the answer is not available in the context, say:
   "The information is not available in the knowledge base."
3. Give concise troubleshooting steps.
4. Explain the likely root causes first.
5. Then provide recommended fixes.


Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
    "answer": response.content,
    "sources": list(
        set(
            os.path.basename(doc.metadata["source"])
            for doc in docs
        )
    ),
    "retrieved_chunks": [
        doc.page_content
        for doc in docs
    ]
    }