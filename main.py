from tools.utils import list_dirs, clone_repo, remove_file
from models.llama_3_1_70B import llama_3_1_70B
from prompts.readme_template import readme_template
import json

MAX_ITERATIONS = 2
# use this to check file length before uploading it to the model, if not, truncate it
MAX_FILE_LINES = 1000


def planner(model, dirs, known_info, already_read, system_prompt_planner):
    planner_prompt = {"files": dirs, "already-seen": already_read,
                      "gathered-info": known_info}
    answer_planner = model.answer(
        system_prompt=system_prompt_planner, prompt=str(planner_prompt), json=True)
    answer_planner = json.loads(answer_planner)
    already_read = answer_planner["already-read"]
    return answer_planner, known_info, already_read


def summarizer(model, files, known_info, system_prompt_summarizer):
    for file_to_check in files:
        with open(file_to_check, "r") as file:
            file_contents = file.read()
        answer_summarizer = model.answer(
            system_prompt=system_prompt_summarizer, prompt=f"Here's what we know now: {known_info}\n\nHere's the file to check: {file_to_check}\n" + file_contents, json=True)

        print(f"The answer from the summarizer: {answer_summarizer}")
        answer_summarizer = json.loads(answer_summarizer)
        known_info = answer_summarizer["known-info"]
    return known_info


def writer(model, known_info, system_prompt_writer, readme_template):
    writer_response = model.answer(
        system_prompt=system_prompt_writer + "\n\n" + readme_template,
        prompt=known_info,
        json=False)
    return writer_response


def validator(model, writer_response, system_prompt_validator, readme_template):
    validator_response = model.answer(
        system_prompt=system_prompt_validator + "\n\n" + readme_template,
        prompt=writer_response,
        json=True
    )
    validator_response = json.loads(validator_response)
    return validator_response["Status"]


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

    repo_url = input(
        "Welcome to AutoREADME! Input the desired github repository:\n")
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
    model = llama_3_1_70B()
    iteration = 0
    ended = False
    skip_planner = False
    skip_summarizer = False
    while (not ended and iteration < MAX_ITERATIONS):
        if (not skip_planner):
            answer_planner, known_info, already_read = planner(model=model, dirs=dirs,
                                                               known_info=known_info, already_read=already_read,
                                                               system_prompt_planner=system_prompt_planner)
            print(f"Planner finished!\n\n {answer_planner['files']}")
        skip_planner = False

        if (not skip_summarizer):
            known_info = summarizer(
                model=model, files=answer_planner["files"], known_info=known_info, system_prompt_summarizer=system_prompt_summarizer)
            print(f"Summarizer finished!\n\n {known_info}")
        skip_summarizer = False

        writer_response = writer(model=model, known_info=known_info,
                                 system_prompt_writer=system_prompt_writer, readme_template=readme_template)
        print(f"Writer finished!\n\n{writer_response}")

        validator_response = validator(model=model, writer_response=writer_response,
                                       system_prompt_validator=system_prompt_validator, readme_template=readme_template)
        print(f"Validator finished with verdict: {validator_response}")

        if (validator_response == "Correct"):
            ended = True
        elif (validator_response == "Format"):
            skip_planner = True
            skip_summarizer = True
        elif (validator_response == "Information"):
            continue
        iteration += 1

    with open("propREADME.md", "w") as file:
        file.write(writer_response)
    remove_file(file_name=repo_name)
