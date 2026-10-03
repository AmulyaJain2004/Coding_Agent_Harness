import json

import tui
from llm import SYSTEM_PROMPT, MODEL, call_llm
from skills import SKILLS
from tools import TOOLS

tui.print_banner(MODEL, SKILLS)
user_input = tui.prompt_input()

messages = [
    {"role":"system","content": SYSTEM_PROMPT},
    {"role":"user","content": user_input}
]

while True:
    with tui.thinking():
        message, usage = call_llm(messages)
    messages.append(message.model_dump(exclude_none=True))

    if message.content:
        tui.render_agent_message(message.content)

    tui.print_usage(usage)

    if not message.tool_calls:
        break

    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        tui.render_tool_call(tool_call.function.name, args)
        result = TOOLS[tool_call.function.name](**args)
        tui.render_tool_result(result)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })
