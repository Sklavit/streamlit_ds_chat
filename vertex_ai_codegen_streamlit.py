import streamlit as st

from vertex_ai_codegen import (
    start_code_generator_chat,
    GENERATION_CONFIG,
    SAFETY_SETTINGS,
)

st.title(
    "Chat with Google Vertex AI to experiment with prompts which could be used for the orchestrator agent."
)

########################################################################
# init chat model

if "vertex_ai_model" not in st.session_state:
    st.session_state["vertex_ai_model"] = "gemini-1.5-flash-001"


if "code_get_chat" not in st.session_state:
    chat = start_code_generator_chat(
        st.secrets["gcs_connections"], model_name=st.session_state["vertex_ai_model"]
    )
    st.session_state.code_get_chat = chat
else:
    chat = st.session_state.code_get_chat

########################################################################
# Working with chat itself

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# streaming is not working with streamlit, exceptions inside `vertexai.generative_models import GenerativeModel`
USE_STREAMING = False

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(
            "Wait for the whole response (streaming not working with Streamlit)..."
        ):
            api_response = chat.send_message(
                prompt,
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS,
                stream=False,
            )
            response = api_response.candidates[0].content.parts[0]._raw_part.text
            st.write(response)

        print(("response:", response))
        st.session_state.messages.append({"role": "assistant", "content": response})
