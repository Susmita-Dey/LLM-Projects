import os
import click
import questionary
from ollama_client import query_ollama
from utils.file_utils import create_project_structure
from utils.logger import log_info, log_step


@click.command()
def generate_project():
    """
    Interactive command line tool to generate a full-stack project.
    """

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

    # project tech stack (will add later)

    log_info(f"\n✨ Generating a {project_type} project: {project_name}...\n")
    log_step("🧠 Querying Ollama to generate code...")

    # Dynamically build prompt
    prompt = f"""
    You are an expert {project_type} engineer. Please generate a {project_type} project with the name {project_name} and the following specifications: {project_spec}.
    The project should be well-structured and include all necessary files and folders. Please provide the code in a zip file format.
    """
    log_info(f"Prompt: {prompt}")
