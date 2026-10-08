import subprocess
from skills import read_skill
from context import note_read
from todos import write_todos

def bash(command):
    # result = subprocess.run(
    #     ["powershell", "-Command", command], capture_output = True, text = True, timeout=60
    # )
    # running under WSL now, so this is real bash — use the host shell directly
    result = subprocess.run(
        command, shell=True, capture_output = True, text = True, timeout=60
    )
    output = result.stdout + result.stderr
    return output if output else "(no output)"

def read_file(path: str) -> str:
    """Read a file and return its content"""
    note_read(path)
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str) -> str:
    """Create a file, or overwrite it if it is already written."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    note_read(path)
    return f"Wrote {path}"

def str_replace(path, old_str, new_str, allow_multi_edit = False):
    """Swap exact text in file. old_str must match exactly once."""
    with open(path, 'r', encoding = "utf-8") as f:
        content = f.read()

    count = content.count(old_str)
    if count == 0:
        return f"Error: old_str was not found in {path}"
    if count > 1 and not allow_multi_edit:
        return (
            f"Error: old_str matches {count} times in {path}."
            "Add surrounding lines to make it unique, "
            "or set allow_multi_edit=True to replace them all."
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content.replace(old_str, new_str))
    note_read(path)
    return f"Replaced {count} match(es) in {path}"

TOOL_SCHEMAS = [
    {
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
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "Open a skill by name and return its full instructions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the skill to read"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create a file, or overwrite it if it already exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write to the file"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "str_replace",
            "description": "Swap exact text in a file. old_str must match exactly once, unless allow_multi_edit is set.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to edit"},
                    "old_str": {"type": "string", "description": "Exact text to replace"},
                    "new_str": {"type": "string", "description": "Text to replace it with"},
                    "allow_multi_edit": {"type": "boolean", "description": "Replace all matches instead of requiring exactly one"},
                },
                "required": ["path", "old_str", "new_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_todos",
            "description": "Replace the whole todo list. Use this to plan and track multi-step work. Exactly one task may be in_progress at a time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string", "description": "The task, e.g. 'Fix the bug'"},
                                "activeForm": {"type": "string", "description": "Present-tense form shown while in progress, e.g. 'Fixing the bug'"},
                                "status": {"type": "string", "enum": ["pending", "in_progress", "done"]},
                            },
                            "required": ["content", "activeForm", "status"],
                        },
                    }
                },
                "required": ["todos"],
            },
        },
    },
]

TOOLS = {
    "bash": bash,
    "read_file": read_file,
    "write_file": write_file,
    "str_replace": str_replace,
    "read_skill": read_skill,
    "write_todos": write_todos,
}

