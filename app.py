import streamlit as st
from rag_pipeline import get_answer

st.set_page_config(
    page_title="GenAI Network Troubleshooting Assistant",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 GenAI Network Troubleshooting Assistant")
st.caption("Powered by RAG + FAISS + Gemini")

show_context = st.checkbox(
    "Show Retrieved Context"
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
prompt = st.chat_input(
    "Ask a networking troubleshooting question..."
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

            result = get_answer(prompt)

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

# Sidebar
with st.sidebar:

    st.header("Example Questions")

    examples = [
        "Why is OSPF not forming adjacency?",
        "BGP neighbor stuck in ACTIVE state",
        "EtherChannel not forming",
        "Hosts in same VLAN cannot communicate",
        "How to troubleshoot STP issues?"
    ]

    for q in examples:
        st.write("•", q)

    st.divider()
 

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()