import sys
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def log_info(message):
    console.print(f"[bold cyan]{message}[/bold cyan]")


def log_step(message):
    console.print(f"[yellow]{message}[/yellow]")


def print_typing(text: str, delay: float = 0.01):
    """
    Prints text with a typing effect.
    :param text: The text to print.
    :param delay: The delay between each character.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    console.print()  # Move to the next line after printing the text


def spinner(message="Thinking..."):
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn(f"[white]{message}"),
        transient=True,
    )
