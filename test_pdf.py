from pdf_ingest import create_pdf_vectorstore

vectorstore = create_pdf_vectorstore(
    "sample_networking_guide.pdf"
)

print("PDF Indexed Successfully!")