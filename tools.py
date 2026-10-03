import subprocess

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

]

TOOLS = {
    "bash": bash,
}

