import os
from dotenv import load_dotenv
from openai import OpenAI

from rules.command import build_prompt

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "google/gemini-1.5-flash"

def generate_message(
    category,
    merchant,
    trigger,
    customer=None,
    tone="professional",
    focus="merchant growth",
):
    prompt = build_prompt(
        category=category,
        merchant=merchant,
        trigger=trigger,
        customer=customer,
        tone=tone,
        focus=focus,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are Vera, Magicpin's merchant growth assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=80,
    )

    return response.choices[0].message.content.strip()