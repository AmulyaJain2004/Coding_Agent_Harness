import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOL_SCHEMAS
from skills import skills_prompt
load_dotenv()

SYSTEM_PROMPT = f"""
You are a coding agent. Your job is to code. Always code.
Use the bash tool to inspect files.
Answer back to the user once exploration is done.

Your current working directory is: {os.getcwd()}

You have skills available. Each one is a set of instructions for a task.
If a skill matches what the user wants, call read_skill first and follow it.

{skills_prompt()}
"""

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    api_key=os.environ["OPENAI_API_KEY"],
)
MODEL = os.environ.get("MODEL", "gemini-3.5-flash")

def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOL_SCHEMAS,
    )
    message = response.choices[0].message
    completion_details = response.usage.completion_tokens_details
    prompt_details = response.usage.prompt_tokens_details
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
        "cached_tokens": getattr(prompt_details, "cached_tokens", None),
    }
    return message, usage
