from groq import Groq
import os

groq_api = "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"

client = Groq(api_key=groq_api)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)