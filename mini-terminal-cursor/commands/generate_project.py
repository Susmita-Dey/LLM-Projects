import os
import click
import questionary
from utils.file_utils import create_project_structure
from utils.logger import log_info, log_step


@click.command()
def generate_project():
    """
    Interactive command line tool to generate a full-stack project.
    """
    from ollama_client import query_ollama  # <-- Move import here

    project_type = questionary.select(
        "🧠 What type of project do you want to create?",
        choices=["full-stack", "backend", "frontend"],
    ).ask()

    project_name = questionary.text(
        "🚀 What is the name of your project? (e.g. my_project)"
    ).ask()

    project_spec = questionary.text(
        "📝 Please provide a brief description of your project (e.g. A simple calculator web app)"
    ).ask()

    log_info(f"\n✨ Generating a {project_type} project: {project_name}...\n")
    log_step("🧠 Querying Ollama to generate code...")

    prompt = f"""
    You are an expert {project_type} engineer. Please generate a {project_type} project with the name {project_name} and the following specifications: {project_spec}.
    
    Output:
    1. Describe what the app is.
    2. Explain the folder structure.
    3. Then output full file code blocks for each file.
    4. Only use minimal required files/folders and no extra text.
Start with a heading like 'Generating Flappy Bird with Python and Pygame...'

    The project should be well-structured with clean, maintainable code.
    """
    log_info(f"Prompt: {prompt}")

    response = query_ollama(prompt)
    log_info("Response received from Ollama.")

    print("\n" + "=" * 60)
    print(response)
    print("=" * 60 + "\n")

    log_step("🗂️ Creating project files...")
    create_project_structure(project_name, response)

    log_info("✅ Done! Your project is ready.\n")
