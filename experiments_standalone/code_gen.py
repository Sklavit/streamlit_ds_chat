from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "Salesforce/codegen-350M-mono"
model = AutoModelForCausalLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

text = "# Write python code to read from csv file with pandas intro dataframe"

completion = model.generate(**tokenizer(text, return_tensors="pt"))

print(tokenizer.decode(completion[0]))
