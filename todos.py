"""The plan. Lives here, not in the transcript, and is re-injected every turn."""

MARKS = {"pending": "[ ]", "in_progress": "[~]", "done": "[x]"}

TODOS = [] # [{"content": ..., "activeForm": ..., "status": ...}]

def write_todos(todos):
    """Replace the whole list. Exactly one task may be in_progress."""
    active = [t for t in todos if t["status"] == "in_progress"]
    if len(active) > 1:
        return f"Error: {len(active)} tasks are in_progress. Only one may be."
    
    TODOS[:] = todos
    return todos_prompt() or "Todo list cleared."

def todos_prompt():
    return "\n".join(f"{MARKS[t['status']]} {t['content']}" for t in TODOS)

def active_form():
    """What the agent is doing right now, for the spinner."""
    for todo in TODOS:
        if todo["status"] == "in_progress":
            return todo["activeForm"]
    return None

def todos_note():
    """Reminder block showing the current plan, re-injected every turn."""
    if not TODOS:
        return ""
    return "\n<todos>\n" + todos_prompt() + "\n</todos>"