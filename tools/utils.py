import subprocess
import os


def clone_repo(repo_url):
    # Prepare and run the git clone command
    command = ["git", "clone", "-q", repo_url]
    subprocess.run(command, check=True)


def remove_file(file_name):
    # Prepare and run the rm -r command
    command = ["rm", file_name, "-rf"]
    subprocess.run(command, check=True)


def list_dirs(directory, prefix=""):
    file_paths = []
    for root, _, files in os.walk(directory):
        # Skip directories and their contents if '.git' is in the path
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths
