import click
import questionary
import config

from commands.generate_project import generate_project
from commands.solve_problem import solve_problem


@click.group()
def cli():
    print("Mini Terminal Cursor CLI is here!")

    if not config.MODE:
        mode = questionary.select(
            "🧠 Choose your OLLAMA mode:", choices=["langchain", "raw (fast)"]
        ).ask()

    config.MODE = mode
    print(f"\n 🚀 Running in [ {mode}] mode\n")


cli.add_command(generate_project)
cli.add_command(solve_problem)

if __name__ == "__main__":
    cli()
