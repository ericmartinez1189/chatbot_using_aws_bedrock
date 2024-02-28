# Importing the required libraries

import streamlit as st
import uuid
import bedrock

# Defining the paths for the user and AI icons

USER_ICON = "images/user-icon.png"
AI_ICON = "images/ai-icon.png"

# Using the session state to store the user id, questions, answers, and input
# Session state is a dictionary that is unique to each user and persists across reruns of the app

if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
else:
    user_id = str(uuid.uuid4())
    st.session_state["user_id"] = user_id

if "llm_chain" not in st.session_state:
    st.session_state["llm_app"] = bedrock
    st.session_state["llm_chain"] = bedrock.bedrock_chain()

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""


# Defining the function to write the top bar of the app
def write_top_bar():
    col1, col2, col3 = st.columns([2, 10, 3])
    with col2:
        header = "Amazon Bedrock Customer assistance Chatbot powered by Titan-Express-V1"
        st.write(f"<h3 class='main-header'>{header}</h3>", unsafe_allow_html=True)
    with col3:
        clear = st.button("Clear Chat")
    return clear


# Writing the top bar
clear = write_top_bar()

# If the clear button is clicked, clear the questions, answers, and input
if clear:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.input = ""
    bedrock.clear_memory(st.session_state["llm_chain"])


# Defining the function to handle the user input
def handle_input():
    # Getting the input from the user
    input = st.session_state.input
    # Running the chain with the user input
    llm_chain = st.session_state["llm_chain"]
    # llm_
    chain = st.session_state["llm_app"]

    # Getting the result and the amount of tokens used
    result, amount_of_tokens = chain.run_chain(llm_chain, input)
    question_with_id = {
        "question": input,
        "id": len(st.session_state.questions),
        "tokens": amount_of_tokens,
    }

    # Appending the question and the answer to the session state
    st.session_state.questions.append(question_with_id)

    # Appending the answer to the session state
    st.session_state.answers.append(
        {"answer": result, "id": len(st.session_state.questions)}
    )
    st.session_state.input = ""

    # Writing the user message and the chat message
def write_user_message(md):
    col1, col2 = st.columns([1, 12])

    with col1:
        st.image(USER_ICON, use_column_width="always")
    with col2:
        st.warning(md["question"])
    st.write(f"Tokens used: {md['tokens']}")


# Defining the function to render the answer from the AI
def render_answer(answer):
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image(AI_ICON, use_column_width="always")
    with col2:
        st.info(answer["response"])

# Defining the function to write the chat answer from the AI 
def write_chat_message(md):
    chat = st.container()
    with chat:
        render_answer(md["answer"])

# Writing the chat history using the session state questions and answers
with st.container():
    for q, a in zip(st.session_state.questions, st.session_state.answers):
        write_user_message(q)
        write_chat_message(a)


# Adding a horizontal line to separate the chat history from the input box
st.markdown("---")

# Adding the input box for the user to ask questions
input = st.text_input(
    "You are talking to an AI, ask any question.", key="input", on_change=handle_input
)