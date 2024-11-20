# utils\directoryTree.py

import os

# Define the project root, output file, and directories to skip
project_root = r"D:\Projects\FoodDome\FoodDome-Backend"
output_file = os.path.join(project_root, "utils", "tree.txt")
skip_dirs = {'.venv', 'venv', 'node_modules', '.pytest_cache', '__pycache__', '.git'}

def generate_tree(directory, prefix=""):
    lines = []
    items = sorted(os.listdir(directory))
    for index, item in enumerate(items):
        path = os.path.join(directory, item)

        # Skip specified directories
        if os.path.isdir(path) and item in skip_dirs:
            continue

        connector = "├── " if index < len(items) - 1 else "└── "
        
        lines.append(f"{prefix}{connector}{item}")
        
        if os.path.isdir(path):
            extension = "│   " if index < len(items) - 1 else "    "
            lines.extend(generate_tree(path, prefix + extension))
    return lines

def write_tree_to_file(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header line for the project root
        f.write(f"{os.path.basename(directory)}\n")
        # Generate and write the tree structure
        tree_lines = generate_tree(directory)
        f.write("\n".join(tree_lines))
    print(f"Project tree saved to {output_file}")

# Generate and save the project tree
write_tree_to_file(project_root, output_file)
