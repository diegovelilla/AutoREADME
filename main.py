from tools.utils import list_dirs, clone_repo, remove_file
from models.groq_model import groq_model
from prompts.readme_template import readme_template
import json
import re
from termcolor import colored

MAX_ITERATIONS = 2
# use this to check file length before uploading it to the model, if not, truncate it
MAX_FILE_LINES = 1000


def planner(model, dirs, known_info, already_read, system_prompt_planner):
    planner_prompt = {"files": dirs, "already-seen": already_read,
                      "gathered-info": known_info}
    answer_planner = model.answer(
        system_prompt=system_prompt_planner, prompt=str(planner_prompt), json=False)
    json_section = re.search(
        r'<output>\s*(.*?)\s*</output>', answer_planner, re.DOTALL)
    answer_planner = json_section.group(1)
    answer_planner = json.loads(answer_planner)
    already_read.extend(answer_planner)
    print(colored(f"Planner: Files to read -> {answer_planner}", "magenta"))
    return answer_planner, known_info, already_read


def summarizer(model, files, known_info, system_prompt_summarizer):
    for file_to_check in files:
        with open(file_to_check, "r") as file:
            file_contents = file.read()
        answer_summarizer = model.answer(
            system_prompt=system_prompt_summarizer, prompt=f"Here's what we know now: {known_info}\n\nHere's the file to check: {file_to_check}\n" + file_contents, json=False)
        json_section = re.search(
            r'<output>\s*(.*?)\s*</output>', answer_summarizer, re.DOTALL)
        answer_summarizer = json_section.group(1)
        print(colored(
            f"Summarizer: Updated known-info template\n{answer_summarizer}", "cyan"))
        known_info = answer_summarizer
    return answer_summarizer


def writer(model, known_info, system_prompt_writer, readme_template):
    answer_writer = model.answer(
        system_prompt=system_prompt_writer + "\n\n" + readme_template,
        prompt=known_info,
        json=False)
    json_section = re.search(
        r'<output>\s*(.*?)\s*</output>', answer_writer, re.DOTALL)
    answer_writer = json_section.group(1)
    return answer_writer


def validator(model, writer_response, system_prompt_validator, readme_template):
    validator_response = model.answer(
        system_prompt=system_prompt_validator + "\n\n" + readme_template,
        prompt=writer_response,
        json=False
    )
    print(validator_response)
    json_section = re.search(
        r'<output>\s*(.*?)\s*</output>', validator_response, re.DOTALL)
    validator_response = json_section.group(1)
    print(colored(f"Validator: My verdict is -> {validator_response}", "red"))
    return validator_response


def initialization(repo_url):
    repo_name = (repo_url.rstrip("/").split("/")[-1])[:-4]
    repo_username = repo_url.rstrip("/").split("/")[-2]
    clone_repo(repo_url)
    with open("./prompts/planner.md", "r") as file:
        system_prompt_planner = file.read()

    with open("./prompts/summarizer.md", "r") as file:
        system_prompt_summarizer = file.read()

    with open("./prompts/writer.md", "r") as file:
        system_prompt_writer = file.read()

    with open("./prompts/validator.md", "r") as file:
        system_prompt_validator = file.read()
    dirs = list_dirs(repo_name)
    return repo_name, repo_username, system_prompt_planner, system_prompt_summarizer, system_prompt_writer, system_prompt_validator, dirs


if __name__ == "__main__":

    # model_name = "mixtral-8x7b-32768"
    # model_name = "llama-3.1-70b-versatile"

    repo_url = input(
        colored("Welcome to AutoREADME! Input the desired github repository:\n", "green"))
    repo_name, repo_username, system_prompt_planner, system_prompt_summarizer, system_prompt_writer, system_prompt_validator, dirs = initialization(
        repo_url=repo_url)

    known_info = f"""
    User: {repo_username}
    Repo name: {repo_name}
    Installation: [Empty]
    Usage: [Empty]
    License: [Empty]
    """
    already_read = []
    # model = groq_model(model_name=model_name)
    model = groq_model()
    iteration = 0
    ended = False
    skip_planner = False
    skip_summarizer = False
    while (not ended and iteration < MAX_ITERATIONS):
        if (not skip_planner):
            print(colored("\nStarting AI Planner...", "green"))
            answer_planner, known_info, already_read = planner(model=model, dirs=dirs,
                                                               known_info=known_info, already_read=already_read,
                                                               system_prompt_planner=system_prompt_planner)
            print(colored("Planner finished!", "green"))
        skip_planner = False

        if (not skip_summarizer):
            print(colored("\nStarting AI Summarizer...", "green"))
            known_info = summarizer(
                model=model, files=answer_planner, known_info=known_info, system_prompt_summarizer=system_prompt_summarizer)
            print(colored(f"Summarizer finished!", "green"))
        skip_summarizer = False

        print(colored("\nStarting AI Writer...", "green"))
        writer_response = writer(model=model, known_info=known_info,
                                 system_prompt_writer=system_prompt_writer, readme_template=readme_template)
        print(colored("Writer finished!", "green"))

        print(colored("\nStarting AI Validator...", "green"))
        validator_response = validator(model=model, writer_response=writer_response,
                                       system_prompt_validator=system_prompt_validator, readme_template=readme_template)
        print(
            colored("Validator finished!", "green"))

        if (validator_response == "Correct"):
            ended = True
        elif (validator_response == "Format"):
            skip_planner = True
            skip_summarizer = True
        iteration = iteration + 1
    if iteration == MAX_ITERATIONS:
        print(
            colored("Ended due to excess of iterations.", "green"))
    with open("myREADME.md", "w") as file:
        file.write(writer_response)
    remove_file(file_name=repo_name)
