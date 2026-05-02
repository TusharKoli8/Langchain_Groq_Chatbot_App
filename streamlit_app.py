## streamlit_app.py
## This is the Streamlit UI wrapper for our LangChain CLI chatbot.
## Instead of running in the terminal with input(), we now have a web-based chat UI.

import streamlit as st
from app.chains import get_chain


# PAGE CONFIG
# The FIRST Streamlit call in the script.

st.set_page_config(
    page_title="Alex – Tech AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# LOAD THE CHAIN ONCE (cached for performance)

# @st.cache_resource tells Streamlit:

# "Run this function only ONCE per server session, then reuse the result for every user interaction."  

# Without this, the LLM connection would be recreated on EVERY message  slow and wasteful.


@st.cache_resource
def load_chain():
    return get_chain()   # same function your main.py used

chain = load_chain()

# SESSION STATE :- stores chat history

# st.session_state persists data across reruns

# (Streamlit reruns the entire script on every user interaction, so we need this to keep history).


if "messages" not in st.session_state:
    st.session_state.messages = []  #(list of role and content)

# UI - HEADER

st.title("🤖 Alex – Tech AI Assistant")
st.caption("Powered by Groq + LangChain · Ask anything tech-related")
st.divider()

# UI - DISPLAY CHAT HISTORY

# Loop through all past messages stored in session state and render them as chat bubbles.
 

for message in st.session_state.messages:
    with st.chat_message(message["role"]):   # "user" or "assistant"
        st.markdown(message["content"])


# UI - CHAT INPUT BOX (appears at the bottom)

# st.chat_input() renders the fixed input bar.
# It returns the user's text only when they hit Enter.

user_input = st.chat_input("Pass your tech query here...")

if user_input:

    # 1. Show the user's message immediately in the chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Save the user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 3. Call the LangChain chain (same as main.py did: chain.invoke(...))
    with st.chat_message("assistant"):
        with st.spinner("Alex is thinking..."):
            response = chain.invoke({"input": user_input})
        st.markdown(response)

    # 4. Save the assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})


# SIDEBAR - Extra info / controls

with st.sidebar:
    st.header("About Alex")
    st.info(
        "Alex is a **tech-only** AI assistant. "
        "Ask questions about programming, software, "
        "hardware, AI, networking, and more.\n\n"
        "For non-tech questions, Alex will politely decline."
    )
    st.divider()

    # Button to wipe the chat history
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()   # re-render the page with empty history
