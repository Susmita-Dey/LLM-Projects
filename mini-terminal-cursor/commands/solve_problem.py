import click
import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import requests
import re

console = Console()


def fetch_leetcode_problem(link):
    # Basic fetch for Leetcode problem statement (HTML scraping)
    try:
        resp = requests.get(link)
        if resp.status_code == 200:
            # Extract problem statement from HTML (very basic, not robust)
            match = re.search(
                r'<div class="content__u3I1 question-content__JfgR">(.*?)</div>',
                resp.text,
                re.DOTALL,
            )
            if match:
                text = re.sub("<.*?>", "", match.group(1))  # Remove HTML tags
                return text.strip()
            else:
                return "Could not extract problem statement from the link."
        else:
            return "Failed to fetch the problem link."
    except Exception as e:
        return f"Error fetching problem: {e}"


@click.command()
def solve_problem():
    """
    Solve coding challenges and Leetcode-style problems using AI.
    """
    from ollama_client import query_ollama

    input_type = questionary.select(
        "How do you want to provide the problem?",
        choices=["Paste a link", "Write a description"],
    ).ask()

    if input_type == "Paste a link":
        link = questionary.text("Paste the problem link (e.g., Leetcode):").ask()
        problem = fetch_leetcode_problem(link)
        console.print(
            Panel(
                f"[bold]Fetched Problem Statement:[/bold]\n{problem}", title="Problem"
            )
        )
    else:
        problem = questionary.text(
            "Describe your coding challenge or paste a Leetcode problem:"
        ).ask()
        console.print(Panel(problem, title="Problem"))

    if not problem:
        console.print("[red]No problem description provided.[/red]")
        return

    console.print("[yellow]Solving your problem with AI...[/yellow]")
    solution = query_ollama(
        f"Solve the following coding challenge. Provide clean, commented code and a brief explanation:\n\n{problem}"
    )

    # Beautify output
    console.print("\n[bold green]--- Solution ---[/bold green]\n")
    console.print(Markdown(solution))
