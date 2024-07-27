from pprint import pprint

import requests
import streamlit as st
from transformers import pipeline

API_TOKEN = st.secrets["HF_API_KEY"]


headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("response", response.status_code)
    return response.json()


data = query(
    {
        "inputs": {
            "past_user_inputs": ["Which movie is the best ?"],
            "generated_responses": ["It's Die Hard for sure."],
            "text": "Can you explain why ?",
        },
    }
)
# Response
# This is annoying
# data.pop("warnings")
pprint(
    (
        data,
        {
            "generated_text": "It's the best movie ever.",
            "conversation": {
                "past_user_inputs": [
                    "Which movie is the best ?",
                    "Can you explain why ?",
                ],
                "generated_responses": [
                    "It's Die Hard for sure.",
                    "It's the best movie ever.",
                ],
            },
            # "warnings": ["Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation."],
        },
    )
)


messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="microsoft/DialoGPT-large")
pipe(messages)
