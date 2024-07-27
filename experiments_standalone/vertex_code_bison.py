import vertexai
from vertexai.language_models import CodeGenerationModel

vertexai.init(project="pivotal-cable-428219-c5", location="us-central1")
parameters = {"candidate_count": 1, "max_output_tokens": 1024, "temperature": 0.9}
model = CodeGenerationModel.from_pretrained("code-bison@002")
response = model.predict(
    prefix="""You are an expert python engineer with data scientist background.
    Write a short snippet of python code, which use pandas to read csv file into dataframe.""",
    **parameters,
)
print(f"Response from Model: {response.text}")
