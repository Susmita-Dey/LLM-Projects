import os
import re
from utils.logger import log_step


def create_project_structure(project_name, response_text):
    project_path = os.path.join("projects", project_name)
    os.makedirs(project_path, exist_ok=True)
    log_step(f"Creating project directory at {project_path}...")

    # Patterns to catch:
    # 1. ```python\n# file: path/to/file.py\n<code>```
    # 2. ```python\n# filename: path/to/file.py\n<code>```
    # 3. ```# path/to/file.py\n<code>```
    patterns = [
        r"```(?:\w+)?\s*#\s*(?:file(?:name)?):\s*(.+?)\n(.*?)```",  # # file: or # filename:
        r"```(?:\w+)?\s*(.+?\.py.*?)\n(.*?)```",  # fallback: looks like a filename
    ]

    matched_files = []

    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.DOTALL)
        for file_path, code in matches:
            file_path = file_path.strip().replace("\\", "/")
            file_path = file_path.replace(" ", "_")
            file_path = file_path.replace(":", "_")
            matched_files.append((file_path, code.strip()))

        if not matched_files:
            log_step("⚠️ No valid file blocks found.")
            return

        for relative_path, code in matched_files:
            # Create directories if they don't exist
            full_path = os.path.join(project_path, relative_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Write code to the file
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code)
                log_step(f"Created {full_path}")
