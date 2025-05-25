import questionary
import config
from rich.console import Console

console = Console()


def main_menu():
    from commands.generate_project import generate_project
    from commands.solve_problem import solve_problem

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Solve a coding problem", "Generate a project", "Exit"],
        ).ask()

        if choice == "Solve a coding problem":
            solve_problem()
        elif choice == "Generate a project":
            generate_project()
        else:
            break

    console.print(f"\n\n[bold]Goodbye![/bold]\n")


if __name__ == "__main__":
    console.print(
        f"\n[cyan][bold]====================================== Mini Terminal Cursor CLI is here! ======================================[/bold][/cyan]\n"
    )

    if not config.MODE:
        mode = questionary.select(
            "🧠 Choose your OLLAMA mode:", choices=["langchain", "raw (fast)"]
        ).ask()
        config.MODE = mode
        print(f"\n 🚀 Running in [ {mode}] mode\n")

    main_menu()
