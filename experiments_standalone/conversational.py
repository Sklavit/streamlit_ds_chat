from transformers import pipeline

generator = pipeline(model="HuggingFaceH4/zephyr-7b-beta")
# Zephyr-beta is a conversational model, so let's pass it a chat instead of a single string
result = generator(
    [{"role": "user", "content": "What is the capital of France? Answer in one word."}],
    do_sample=False,
    max_new_tokens=2,
)

# [{'generated_text': [{'role': 'user', 'content': 'What is the capital of France? Answer in one word.'},
#                     {'role': 'assistant', 'content': 'Paris'}]}]

print(result)
