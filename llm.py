import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

user_input = input("Enter your prompt>")

SYSTEM_PROMPT = """
You are a coding agent. Your job is to code. Always code.
"""

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    api_key=os.environ["OPENAI_API_KEY"],
)
MODEL = os.environ.get("MODEL", "gemini-3.5-flash")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role":"user","content": user_input}
    ]
)


output = response.choices[0].message.content

completion_details = response.usage.completion_tokens_details
prompt_details = response.usage.prompt_tokens_details

usage = {
    "prompt_tokens": response.usage.prompt_tokens,
    "completion_tokens": response.usage.completion_tokens,
    "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
    "cached_tokens": getattr(prompt_details, "cached_tokens", None)
}

print("\nAgent: ", output, "\n")
print(usage)