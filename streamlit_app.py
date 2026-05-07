import streamlit as st
from app.chains import get_chain

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Alex – Tech AI Assistant",
    page_icon="🤖",
    layout="wide" # Changed to wide to give the sidebar more room
)

# 2. LOAD THE CHAIN (Cached)
@st.cache_resource
def load_chain():
    return get_chain()

chain = load_chain()

# 3. INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR SECTION ---
with st.sidebar:
    st.title("Chat History")
    
    # This is the part that was missing/not working:
    if not st.session_state.messages:
        st.write("No chat history available.")
    else:
        # Loop through messages and display ONLY user questions in the sidebar
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.text(f"💬 {msg['content'][:30]}...") # Shows first 30 chars

    st.divider()
    st.header("About Alex")
    st.info(
        "Alex is a **tech-only** AI assistant. "
        "Ask questions about programming, software, hardware, and more."
    )
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🤖 Alex – Tech AI Assistant")
st.caption("Powered by Groq + LangChain · Ask anything tech-related")
st.divider()

# Display existing messages in the main chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_input = st.chat_input("Pass your tech query here...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Alex is thinking..."):
            # Ensure chain.invoke returns a string. 
            # If it returns an object, use response.content or str(response)
            response = chain.invoke({"input": user_input})
            # Handle LangChain objects if necessary (e.g., response.content)
            final_text = response if isinstance(response, str) else response.content
            
        st.markdown(final_text)
    
    st.session_state.messages.append({"role": "assistant", "content": final_text})
    
    # Rerun to update the sidebar history immediately
    st.rerun()