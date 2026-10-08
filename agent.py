import json
import tui
from llm import SYSTEM_PROMPT, MODEL, call_llm
from skills import SKILLS
from tools import TOOLS
from context import reminder

tui.print_banner(MODEL, SKILLS)

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    user_input = tui.prompt_input()
    if user_input.strip().lower() in ("exit", "quit"):
        break
    messages.append({"role": "user", "content": user_input})

    while True:
        with tui.thinking():
            message, usage = call_llm(messages + [reminder()])

        messages.append(message.model_dump(exclude_none=True))

        if message.content:
            tui.render_agent_message(message.content)

        tui.print_usage(usage)

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            tui.render_tool_call(tool_call.function.name, args)
            try:
                result = TOOLS[tool_call.function.name](**args)
            except Exception as e:
                result = f"Error: {e}"
            tui.render_tool_result(result)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
