from pprint import pprint

# Use a pipeline as a high-level helper
from transformers import pipeline

oracle = pipeline("text2text-generation", model="describeai/gemini")
# - `"question-answering"`: will return a [`QuestionAnsweringPipeline`].
# - `"text2text-generation"`: will return a [`Text2TextGenerationPipeline`].

# QuestionAnsweringPipeline

# result = oracle(question="Write a short snippet of python code, which use pandas to read csv file into dataframe.", context="I am an expert Python engineer.")
result = oracle(
    inputs=[
        "Write a short snippet of python code, which use pandas to read csv file into dataframe.",
        "I am an expert Python engineer.",
    ],
    max_lenght=1000,
    max_new_tokens=1000,
)

pprint(result)

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# tokenizer = AutoTokenizer.from_pretrained("describeai/gemini")
# model = AutoModelForSeq2SeqLM.from_pretrained("describeai/gemini")
