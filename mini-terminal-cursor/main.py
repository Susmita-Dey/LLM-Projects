import questionary
import config


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
            print("Goodbye!")
            break


if __name__ == "__main__":
    print("Mini Terminal Cursor CLI is here!")

    if not config.MODE:
        mode = questionary.select(
            "🧠 Choose your OLLAMA mode:", choices=["langchain", "raw (fast)"]
        ).ask()
        config.MODE = mode
        print(f"\n 🚀 Running in [ {mode}] mode\n")

    main_menu()
