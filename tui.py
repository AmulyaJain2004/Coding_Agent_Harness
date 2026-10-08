"""Terminal UI layer: all rich/colorama rendering lives here.

agent.py drives the conversation; it calls into this module to display
things instead of calling print() directly.
"""

import json
import os
import sys

from colorama import init as colorama_init
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from todos import active_form

# Windows consoles default stdout/stderr to the system codepage (e.g. cp1252),
# which can't encode the unicode glyphs rich writes out (box borders, etc).
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

# colorama patches stdout so raw ANSI escapes (e.g. from subprocess output
# the bash tool returns) still render correctly on legacy Windows consoles.
# legacy_windows=False tells rich to emit plain ANSI instead of calling the
# Win32 console API directly, so colorama's translation is the only one
# in the pipeline and the two don't fight each other.
colorama_init(autoreset=True)

ACCENT = "bright_cyan"
console = Console(legacy_windows=False)


def print_banner(model, skills):
    body = Text()
    body.append("model   ", style="dim")
    body.append(f"{model}\n", style="bold yellow")
    body.append("cwd     ", style="dim")
    body.append(f"{os.getcwd()}\n", style="white")
    body.append("skills  ", style="dim")
    if skills:
        body.append(f"{len(skills)} loaded  ", style="bold green")
        body.append(", ".join(skills), style="green")
    else:
        body.append("none found", style="dim italic")

    console.print(
        Panel(
            body,
            title="[bold white] Coding Agent Harness [/]",
            border_style=ACCENT,
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def prompt_input():
    return console.input(f"\n[bold {ACCENT}]Enter your prompt ›[/bold {ACCENT}] ")


def thinking():
    """Context manager that shows a spinner while the LLM is responding.

    Shows the current in_progress todo, if any, instead of a generic label.
    """
    text = active_form() or "thinking..."
    return console.status(f"[bold green]{text}[/]", spinner="dots")


def render_agent_message(content):
    console.print(
        Panel(
            Markdown(content),
            title="[bold green]agent[/]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def print_usage(usage):
    parts = [
        f"[dim]prompt[/] [cyan]{usage['prompt_tokens']}[/]",
        f"[dim]completion[/] [cyan]{usage['completion_tokens']}[/]",
    ]
    if usage.get("cached_tokens"):
        parts.append(f"[dim]cached[/] [green]{usage['cached_tokens']}[/]")
    if usage.get("reasoning_tokens"):
        parts.append(f"[dim]reasoning[/] [magenta]{usage['reasoning_tokens']}[/]")
    console.print(Text.from_markup("  ".join(parts)))


def render_tool_call(name, args):
    syntax = Syntax(
        json.dumps(args, indent=2),
        "json",
        theme="ansi_dark",
        background_color="default",
        word_wrap=True,
    )
    console.print(
        Panel(
            syntax,
            title=f"[bold yellow]⚙ {name}[/]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 1),
        )
    )


def render_tool_result(result):
    text = result if len(result) < 4000 else result[:4000] + "\n... (truncated)"
    console.print(
        Panel(
            Text(text),
            title="[dim]output[/]",
            border_style="grey50",
            box=box.ROUNDED,
            padding=(0, 1),
        )
    )
