import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.set_page_config(page_title="Domain Expert Chatbot")

st.title("🧠 Domain Expert Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "domain_set" not in st.session_state:
    st.session_state.domain_set = False
if "model" not in st.session_state:
    st.session_state.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Domain input (only once)
if not st.session_state.domain_set:
    domain = st.text_input("Enter the domain (e.g., cricket, science):", key="domain_input")
    if domain:
        chat_template = ChatPromptTemplate([
            ('system', 'You are a helpful {domain} expert who explains things in short and simple terms.')
        ])
        prompt_value = chat_template.invoke({'domain': domain})
        system_message = prompt_value.to_messages()[0]
        st.session_state.chat_history.append(system_message)
        st.session_state.domain_set = True
        st.rerun()  # reload with domain set
    st.stop()

# Display chat history
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)

# User input and response
if prompt := st.chat_input("Ask a question or type 'exit' to end"):
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.model.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=response.content))

    with st.chat_message("assistant"):
        st.markdown(response.content)
