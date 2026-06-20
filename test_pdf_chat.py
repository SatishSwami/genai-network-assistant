from pdf_ingest import create_pdf_vectorstore
from pdf_chat import ask_pdf_question

vectorstore = create_pdf_vectorstore(
    "sample_networking_guide.pdf"
)

result = ask_pdf_question(
    vectorstore,
    "Why does OSPF adjacency fail?"
)

print("\nANSWER:\n")

print(result["answer"])