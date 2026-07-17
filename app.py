import streamlit as st
from agent import Agent

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Agent")

if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "messages" not in st.session_state:
    st.session_state.messages = []


def display_message(role, content):
    with st.chat_message(role):
        # Check if it's an image response
        if isinstance(content, str) and content.startswith("IMAGE::"):
            parts = content.split("::", 2)
            image_url = parts[1]
            caption = parts[2] if len(parts) > 2 else ""
            st.image(image_url, use_column_width=True)
            if caption:
                st.caption(caption)
        else:
            st.markdown(content)



# Display previous messages
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# User input
prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    display_message("user", prompt)

    response = st.session_state.agent.run_agent(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    display_message("assistant", response)