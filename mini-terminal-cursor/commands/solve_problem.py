import click
import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


@click.command()
def solve_problem():
    """
    Solve coding challenges and Leetcode-style problems using AI.
    """
    from ollama_client import query_ollama

    problem = questionary.text(
        "Describe your coding challenge or paste the full problem statement:"
    ).ask()

    if not problem or not problem.strip():
        console.print("[red]No problem description provided. Aborting.[/red]")
        return

    language = questionary.select(
        "💻 Choose the programming language for the solution:",
        choices=[
            "Python",
            "Java",
            "JavaScript",
            "TypeScript",
            "C",
            "C++",
            "Go",
            "Rust",
            "PHP",
            "Other",
        ],
    ).ask()

    if language == "Other":
        language = questionary.text(
            "Please specify your preferred programming language"
        ).ask()

    console.print(Panel(problem, title="Problem", highlight=True))
    console.print(f"[cyan]Language selected:[/cyan] [bold]{language}[/bold]")

    console.print("[yellow]🧠 Solving your problem with AI...[/yellow]")
    solution = query_ollama(
        f"""You are an expert competitive programmer.
        Solve the following coding challenge in {language}.

        1. First, explain your approach step by step.
        2. Then, write a function with the correct signature as required by the problem.
        3. Ensure your code passes all edge cases and is efficient.
        4. After the code, provide at least two sample test cases and their expected outputs.

        Problem statement:
        {problem}
        """
    )

    # Beautify output
    console.print("\n[bold green]--- Solution ---[/bold green]\n")
    console.print(Markdown(solution))
