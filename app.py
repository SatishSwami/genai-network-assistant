import streamlit as st
from rag_pipeline import get_answer

st.set_page_config(
    page_title="GenAI Network Troubleshooting Assistant",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 GenAI Network Troubleshooting Assistant")
st.write("Ask Cisco troubleshooting questions using RAG + FAISS + Gemini")

query = st.text_input(
    "Ask your question:",
    placeholder="Why is OSPF not forming adjacency?"
)

if st.button("Ask"):

    if query:

        with st.spinner("Searching knowledge base..."):

            result = get_answer(query)

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            for source in result["sources"]:
                st.write(f"• {source}")