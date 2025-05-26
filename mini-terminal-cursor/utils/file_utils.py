import os
import re
from utils.logger import log_step


def create_project_structure(project_name, response_text):
    project_path = os.path.join("projects", project_name)
    os.makedirs(project_path, exist_ok=True)
    log_step(f"Creating project directory at {project_path}...")

    # --- Improved: Parse and create only subfolders from "Folder Structure" section ---
    folder_structure_match = re.search(
        r"Folder Structure:?[\s\S]*?(```[\s\S]*?```|$)",  # match until code block or end
        response_text,
        re.IGNORECASE,
    )
    if folder_structure_match:
        # Extract lines from the folder structure block (inside ``` or indented)
        folder_block = folder_structure_match.group(1)
        if folder_block.startswith("```"):
            folder_lines = folder_block.strip("`").splitlines()
        else:
            folder_lines = folder_block.splitlines()
        # Remove empty and whitespace-only lines
        folder_lines = [line.strip() for line in folder_lines if line.strip()]
        # Remove the root folder line if present (e.g., 'calc/')
        if folder_lines and (
            folder_lines[0].rstrip("/").lower() == project_name.lower()
            or folder_lines[0].rstrip("/").lower() == f"{project_name.lower()}"
        ):
            folder_lines = folder_lines[1:]
        # Only create subfolders (ending with '/')
        for line in folder_lines:
            # Remove tree/indentation markers (|---, └──, etc.)
            clean_line = re.sub(r"^[\|\-`*\. ]*", "", line)
            if clean_line.endswith("/") and clean_line != "/":
                folder = clean_line.strip("`")
                folder_path = os.path.join(project_path, folder)
                if os.path.normpath(folder_path) != os.path.normpath(project_path):
                    os.makedirs(folder_path, exist_ok=True)
                    log_step(f"Created folder {folder_path}")

    # Patterns to catch:
    # 1. ```<lang>\n// filepath: path/to/file\n<code>```
    # 2. ```python\n# file: path/to/file.py\n<code>```
    # 3. ```python\n# filename: path/to/file.py\n<code>```
    # 4. ```<lang>\n<filename>\n<code>```
    patterns = [
        r"```(?:\w+)?\s*//\s*filepath:\s*([^\n]+)\n(.*?)```",  # // filepath: path/to/file
        r"```(?:\w+)?\s*#\s*(?:file(?:name)?):\s*([^\n]+)\n(.*?)```",  # # file: or # filename:
        r"```(?:\w+)?\s*([^\n]+?\.\w+)\n(.*?)```",  # fallback: filename with possible path
    ]

    matched_files = []

    illegal_chars = set('<>:"\\|?*\n\r\t')

    def is_valid_filename(filename):
        if not filename:
            return False
        if filename.startswith("/") or filename.startswith("\\"):
            return False
        if filename.strip().startswith("|") or filename.strip().startswith("---"):
            return False
        if filename.strip().startswith("#") or filename.strip().startswith("-"):
            return False
        if "###" in filename:
            return False
        if any(c in illegal_chars for c in filename):
            return False
        if filename.strip().startswith(".") and not filename.strip().startswith("./"):
            return False
        return True

    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.DOTALL)
        for file_path, code in matches:
            file_path = file_path.strip().replace("\\", "/")
            file_path = file_path.replace(" ", "_")
            file_path = file_path.replace(":", "_")
            file_path = file_path.splitlines()[0]
            if not is_valid_filename(file_path):
                continue
            code = code.strip()
            if not code or code.startswith("```"):
                continue  # skip empty or malformed code blocks
            matched_files.append((file_path, code))
        if matched_files:
            break  # Stop at the first pattern that matches files

    if not matched_files:
        log_step(
            "⚠️ No valid file blocks found. (Debug: patterns tried, no matches with valid filenames)"
        )
        return

    for relative_path, code in matched_files:
        full_path = os.path.join(project_path, relative_path)
        parent_dir = os.path.dirname(full_path)
        if parent_dir and parent_dir != project_path:
            os.makedirs(parent_dir, exist_ok=True)
        # Write code to the file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code)
            log_step(f"Created {full_path}")
