import streamlit as st

import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from google.oauth2.service_account import Credentials

from datetime import datetime


st.title("Stub of DS chat with Google Vertex AI")

########################################################################
# init chat model

chat = None

if "vertex_ai_model" not in st.session_state or chat is None:
    st.session_state["vertex_ai_model"] = "gemini-1.5-flash-001"

    credentials = Credentials.from_service_account_info(st.secrets["gcs_connections"])
    vertexai.init(
        project="pivotal-cable-428219-c5",
        location="us-central1",
        credentials=credentials,
    )
    model = GenerativeModel(
        st.session_state[
            "vertex_ai_model"
        ],  # by default it will be "gemini-1.5-flash-001",
        system_instruction=[
            "You are an expert python engineer with data scientist background."
            "If the user's question needs code generation, respond with: <CODE>"
            "If the user's question needs drawing a chart, respond with: <CHART>"
        ],
    )
    chat = model.start_chat()

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

#####################################


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
        if USE_STREAMING:
            api_response_stream = chat.send_message(
                [prompt],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )

            def stream_data():
                for api_response in api_response_stream:
                    chunk = api_response.candidates[0].content.parts[0]._raw_part.text
                    print(f"{datetime.now()}: {chunk}")
                    yield chunk

            response = st.write_stream(stream_data)
        else:
            with st.spinner(
                "Wait for the whole response (streaming not working with Streamlit)..."
            ):
                api_response = chat.send_message(
                    [prompt],
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=False,
                )
                response = api_response.candidates[0].content.parts[0]._raw_part.text
                st.write(response)

        print(("response:", response))
        st.session_state.messages.append({"role": "assistant", "content": response})
