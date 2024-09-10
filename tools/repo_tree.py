import subprocess
import os


def clone_repo(repo_url):
    # Prepare and run the git clone command
    command = ["git", "clone", "-q", repo_url]
    subprocess.run(command, check=True)


def remove_repo(repo_name):
    # Prepare and run the rm -r command
    command = ["rm", repo_name, "-rf"]
    subprocess.run(command, check=True)


def generate_tree(directory, prefix=""):
    tree = ""
    # List all entries in the directory
    entries = os.listdir(directory)
    entries.sort()  # Sort entries to maintain order (alphabetical)

    # Traverse the entries
    for index, entry in enumerate(entries):
        if (entry != ".git"):
            path = os.path.join(directory, entry)
            connector = "└── " if index == len(entries) - 1 else "├── "
            tree += f"{prefix}{connector}{entry}\n"

            if os.path.isdir(path):
                # Recursively add subdirectories and files
                extension = "    " if index == len(entries) - 1 else "│   "
                tree += generate_tree(path, prefix + extension)

    return tree
