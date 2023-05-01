# utils.py
import openai
import os
from dotenv import load_dotenv
import time
import textwrap

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
model_engine = "gpt-3.5-turbo"

def generate_message(prompt, yield_steps=3):
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

    # Split the message into 'yield_steps' number of chunks
    message_chunks = textwrap.wrap(message, len(message) // yield_steps)

    # Yield each chunk as a partial response
    for chunk in message_chunks:
        yield chunk
        time.sleep(1)  # Add a small delay to simulate streaming