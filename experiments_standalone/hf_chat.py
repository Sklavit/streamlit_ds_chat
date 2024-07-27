from pprint import pprint

import requests
import streamlit as st

# Your Hugging Face API key
API_TOKEN = st.secrets["HF_API_KEY"]

# API URL for Hugging Face models
API_URL = "https://api-inference.huggingface.co/models/gpt2"
# API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

# Headers for authentication
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# Function to query the model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Example input
data = {
    # "inputs": "Can you explain the theory of relativity in simple terms?"
    # "inputs": "I have a dataset with columns ID, name, company, price. I need to make an aggragated dataset with average price by company. Write python pandas code to do this. Responde with pyhton code only."
    # "inputs": "Write python code to read file into pandas dataframe.",
    "inputs": {
        "text": "Write python code to read file into pandas dataframe.",
    },
    # "max_length": 10000,
    "wait_for_model": True,
}

# Get the response
response = query(data)
pprint(response)  # only field: generated_text

#############
# from transformers import pipeline  # conda install pytorch
#
# # Load the model and tokenizer
# generator = pipeline('text-generation', model='gpt2')
#
# # Generate text
# result = generator("Can you explain the theory of relativity in simple terms?", max_length=50)
# pprint(result)
