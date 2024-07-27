"""
pip install --upgrade google-cloud-aiplatform
gcloud auth application-default login

Command 'gcloud' not found, but can be installed with:
sudo snap install google-cloud-cli  # version 483.0.0, or
sudo snap install google-cloud-sdk  # version 483.0.0

#################333
Credentials saved to file: [/home/s-nechuiviter/.config/gcloud/application_default_credentials.json]

These credentials will be used by any library that requests Application Default Credentials (ADC).
WARNING:
Cannot find a quota project to add to ADC. You might receive a "quota exceeded" or "API not enabled" error. Run $ gcloud auth application-default set-quota-project to add a quota project.
"""

import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models

# import streamlit as st

from google.oauth2.service_account import Credentials

creds = {}

credentials = Credentials.from_service_account_info(
    creds
)  # st.secrets["gcs_connections"])


def multiturn_generate_content():
    vertexai.init(
        project="pivotal-cable-428219-c5",
        location="us-central1",
        credentials=credentials,
    )
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=[
            """You are an expert python engineer with data scientist background."""
        ],
    )
    chat = model.start_chat()
    print(
        chat.send_message(
            [text1_1],
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
    )


text1_1 = """Write a short snippet of python code, which use pandas to read csv file into dataframe. Return only code, nothing else. So I could copy the response, so I could copy it into python module."""

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

multiturn_generate_content()

"""
Example results:

candidates {
  content {
    role: "model"
    parts {
      text: "```python\nimport pandas as pd\ndf = pd.read_csv(\'your_file.csv\')\n```"
    }
  }
  finish_reason: STOP
  safety_ratings {
    category: HARM_CATEGORY_HATE_SPEECH
    probability: NEGLIGIBLE
    probability_score: 0.06632687151432037
    severity: HARM_SEVERITY_NEGLIGIBLE
    severity_score: 0.10017222911119461
  }
  safety_ratings {
    category: HARM_CATEGORY_DANGEROUS_CONTENT
    probability: NEGLIGIBLE
    probability_score: 0.20134170353412628
    severity: HARM_SEVERITY_NEGLIGIBLE
    severity_score: 0.07599521428346634
  }
  safety_ratings {
    category: HARM_CATEGORY_HARASSMENT
    probability: NEGLIGIBLE
    probability_score: 0.193451926112175
    severity: HARM_SEVERITY_NEGLIGIBLE
    severity_score: 0.09334687888622284
  }
  safety_ratings {
    category: HARM_CATEGORY_SEXUALLY_EXPLICIT
    probability: NEGLIGIBLE
    probability_score: 0.06816437095403671
    severity: HARM_SEVERITY_NEGLIGIBLE
    severity_score: 0.05155818909406662
  }
}
usage_metadata {
  prompt_token_count: 52
  candidates_token_count: 24
  total_token_count: 76
}


"""
