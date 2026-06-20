import streamlit as st
from rag_pipeline import get_answer

from pdf_ingest import create_pdf_vectorstore
from pdf_chat import ask_pdf_question

st.set_page_config(
    page_title="GenAI Network Troubleshooting Assistant",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 GenAI Network Troubleshooting Assistant")

st.markdown(
    """
    Retrieve networking knowledge or chat with your own PDF documents using
    RAG, FAISS, and Gemini.
    """
)

# Sidebar
with st.sidebar:
    st.header("Mode")

    mode = st.radio(
    "Choose Mode",      
    [
        "Knowledge Base",
        "Upload PDF"
    ]
    )

    st.divider()

    show_context = st.checkbox(
        "Show Retrieved Context"
    )

    st.header("Example Questions")

    examples = [
        "Why is OSPF not forming adjacency?",
        "BGP neighbor stuck in ACTIVE state",
        "EtherChannel not forming",
        "Hosts in same VLAN cannot communicate",
        "How to troubleshoot STP issues?"
    ]

    for q in examples:
        st.markdown(f"• {q}")

    st.divider()

    st.header("Project Info")

    st.markdown("""
     - LLM: Gemini 2.5 Flash
     - Vector DB: FAISS
     - Embeddings: MiniLM-L6-v2
     - Framework: LangChain
     """)
    
    st.divider()
 
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

uploaded_pdf = None

if "pdf_vectorstore" not in st.session_state:
    st.session_state.pdf_vectorstore = None

if mode == "Upload PDF":

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        with open(
            "temp_uploaded.pdf",
            "wb"
        ) as f:

            f.write(
                uploaded_pdf.getbuffer()
            )

        if st.session_state.pdf_vectorstore is None:

            with st.spinner(
                "Processing PDF..."
            ):

                st.session_state.pdf_vectorstore = (
                    create_pdf_vectorstore(
                        "temp_uploaded.pdf"
                    )
                )
                st.success(
                  f"Loaded: {uploaded_pdf.name}"
     ) 

            st.success(
                "PDF indexed successfully!"
            )   
    


# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and "sources" in message
        ):
            st.markdown("**Sources:**")
            for source in message["sources"]:
                st.write(f"• {source}")

# Chat Input
placeholder = (
    "Ask about the uploaded PDF..."
    if mode == "Upload PDF"
    else "Ask a networking troubleshooting question..."
)

prompt = st.chat_input(
    placeholder
)

if prompt:

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Searching knowledge base..."):

            if mode == "Knowledge Base":

               result = get_answer(prompt)

            else:

                if st.session_state.pdf_vectorstore is None:

                   st.error(
                      "Please upload a PDF first."
                   )

                   st.stop()

                result = ask_pdf_question(
                  st.session_state.pdf_vectorstore,
                  prompt
                )

                result["sources"] = [
                      "Uploaded PDF"
                ]

                result["retrieved_chunks"] = (
                     result["chunks"]
       )

            st.markdown(result["answer"])
            if show_context:

                st.markdown("---")
                st.markdown("### Retrieved Context")

                for i, chunk in enumerate(
                    result["retrieved_chunks"],
                    start=1
                ):
                    st.markdown(
                        f"#### Chunk {i}"
                    )

                    with st.expander(
                        f"Retrieved Chunk {i}"
                    ):
                        st.code(chunk)

            st.markdown("**Sources:**")

            for source in result["sources"]:
                st.write(f"• {source}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        }
    )

