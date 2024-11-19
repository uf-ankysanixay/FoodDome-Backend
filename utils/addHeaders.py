# utils\addHeaders.py

import os

# Define the project root and the directories to skip
project_root = r"D:\Projects\FoodDome\FoodDome-Backend"
skip_dirs = {'.venv', 'venv', '.pytest_cache', '__pycache__', '.extras'}

def clean_and_add_header(file_path):
    # Header format with file path relative to project root
    header = f"# {os.path.relpath(file_path, project_root)}\n\n"
    
    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        
        # Find the first line with code
        first_code_index = 0
        for i, line in enumerate(lines):
            # Check if the line is not a comment or empty (ignores docstrings and comments)
            if line.strip() and not line.strip().startswith("#"):
                first_code_index = i
                break
        
        # Remove all lines before the first line of code and add header
        cleaned_content = header + ''.join(lines[first_code_index:])
        
        # Write the updated content back to the file
        file.seek(0)
        file.write(cleaned_content)
        file.truncate()

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        # Update dirs to skip specified directories, which prevents os.walk from descending into them
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                clean_and_add_header(file_path)

# Start processing from the project root
process_directory(project_root)
print("Headers added and cleaned successfully.")