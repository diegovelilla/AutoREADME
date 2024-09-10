from tools.repo_tree import generate_tree, clone_repo, remove_repo
from models.llama_3_1_70B import llama_3_1_70B
from prompts.readme_template import readme_template
import json


def initialize(repo_url):
    repo_name = (repo_url.rstrip("/").split("/")[-1])[:-4]
    print(repo_name)

    clone_repo(repo_url)

    system_prompt_parser = ""
    system_prompt_summarizer = ""
    with open("./prompts/parser.md", "r") as file:
        system_prompt_parser = file.read()

    with open("./prompts/summarizer.md", "r") as file:
        system_prompt_summarizer = file.read()

    with open("./prompts/writer.md", "r") as file:
        system_prompt_writer = file.read()

    tree = generate_tree(repo_name)
    return repo_name, system_prompt_parser, system_prompt_summarizer, system_prompt_writer, tree


if __name__ == "__main__":

    repo_name, system_prompt_parser, system_prompt_summarizer, system_prompt_writer, tree = initialize(
        repo_url="https://github.com/diegovelilla/3-SAT-solver.git")

    first_prompt = {"tree": tree, "seen": []}
    model = llama_3_1_70B()
    answer_parser = model.answer(
        system_prompt=system_prompt_parser, prompt=str(first_prompt))
    print(answer_parser)
    answer_parser = json.loads(answer_parser)
    for file_to_check in answer_parser["files-to-check"]:

        with open(repo_name+"/"+file_to_check, "r") as file:
            file_contents = file.read()

        answer_summarizer = model.answer(
            system_prompt=system_prompt_summarizer, prompt=file_contents)
        print(f"The answer from the summarizer: {answer_summarizer}")
        answer_summarizer = json.loads(answer_summarizer)

        summary = answer_summarizer["summary"]
        with open("logs.txt", "a") as file:
            file.write(summary + "\n")
    print("Finished")

    with open("logs.txt", "r") as file:
        logs = file.read()

    writer_response = model.answer(
        system_prompt=system_prompt_writer + "\n\n" + readme_template, prompt=logs+f"The title of the repo is {repo_name}")
    print(writer_response[:100])
    with open("README.md", "w") as file:
        file.write(writer_response)
    remove_repo(repo_name=repo_name)
