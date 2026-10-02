import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
load_dotenv()

user_input = input("Enter your prompt>")

SYSTEM_PROMPT = """
You are a coding agent. Your job is to code. Always code.
Use the bash tool to inspect files.
Answer back to the user once exploration is done.
"""

BASH_TOOL = {
    "type": "function",
    "function": {
        "name": "bash",
        "description": "Run a shell command and return its output",
        "parameters": {
            "type": "object",
            "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run",
                    }
                },
            "required": ["command"]
        }
    }
}

def bash(command):
    result = subprocess.run(["powershell", "-Command", command], capture_output = True, text = True) # for powershell
#     result = subprocess.run(command, shell = True, capture_output = True, text = True)
    return result.stdout + result.stderr

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    api_key=os.environ["OPENAI_API_KEY"],
)
MODEL = os.environ.get("MODEL", "gemini-3.5-flash")

response = client.chat.completions.create(
    model=MODEL,
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role":"user","content": user_input}
    ],
    tools=[BASH_TOOL]
)

message = response.choices[0].message
output = message.content
completion_details = response.usage.completion_tokens_details
prompt_details = response.usage.prompt_tokens_details

usage = {
    "prompt_tokens": response.usage.prompt_tokens,
    "completion_tokens": response.usage.completion_tokens,
    "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
    "cached_tokens": getattr(prompt_details, "cached_tokens", None)
}

print("\nAgent: ", output, "\n")

if message.tool_calls:
    tool_call = message.tool_calls[0]
    command = json.loads(tool_call.function.arguments)["command"]
    print("Tool: bash", command)
    print(bash(command), "\n")

print(usage)