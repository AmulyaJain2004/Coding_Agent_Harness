import subprocess
from skills import read_skill
from context import note_read

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
    note_read(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
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
    }
]

TOOLS = {
    "bash": bash,
    "read_file": read_file,
    "read_skill": read_skill,
}

