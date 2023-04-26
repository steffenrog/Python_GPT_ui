# utils.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
model_engine = "gpt-3.5-turbo"

def generate_message(prompt):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=conversation,
        temperature=0.8,
        max_tokens=1024,
        n=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    message = response.choices[0].message['content'].strip()
    return message