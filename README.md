# AutoREADME: Automatize Project Documentation

> [!Note]  
> I've put a lot of time and effort on this project because I believe it can help lots of developers.
>
> If you find this project any useful or interesting and have an idea that might improve it, make sure to collaborate or let me know.
>
> Would really appreciate if you ⭐ or 🔁 the repository in order to bring more attention to it.
> 
> All help is very much welcomed :)))

## Table of Contents
- [Overview](#overview)
  - [Models](#models)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
  - [AI Planner](#ai-planner)
  - [AI Summarizer](#ai-summarizer)
  - [AI Writer](#ai-writer)
  - [AI Validator](#ai-validator)
- [Zero-Shot Chain of Reasoning](#zero-shot-chain-of-thought)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
AutoREADME is an AI powered tool that generates a very definitive version of a README.md file for any given repository.

### Models
- LLaMA 3.1 70B from *Groq*

## Installation
To install AutoREADME and its dependencies, run the following commands:
```bash
git clone https://github.com/userNanni/AutoREADME.git
cd AutoREADME
pip install -r requirements.txt
```
Make sure to change the following line with your own Groq API key in the config/.env file:
```
GROQ_API_KEY="your_api_key_here"
MODEL_NAME="your_model"
```

## Usage:
To use AutoREADME, simply run the following command:

```bash
python3 main.py
```

Then, you be greeted with the following message:

```bash
Welcome to AutoREADME! Input the desired github repository:
```

Now just type the desired GitHub repository you want to create the README file for:

```bash
https://github.com/diegovelilla/AutoREADME.git
```

> [!Warning]  
> When copy-pasting the url, make sure it ends in **.git**.

## Workflow

![Workflow](https://github.com/diegovelilla/AutoREADME/blob/main/media/workflow.png)

In this workflow we are giving 4 different personas to the AI model:
- An **AI Planner**.
- An **AI Researcher**.
- An **AI Writer**.
- An **AI Validator**.

The workflow starts by cloning the given project and generating a list of all files (except the ones inside the .git folder).

The list is then passed to the **AI Planner**.

---

### AI Planner

The first AI agent is the **AI Planner**.

GOAL:
- Predicting which of the files inside the project may contain more information about the project based on their pahtfile.

INPUT:
- A list of all files inside the given repository.
- A list of already seen files (starting as an empty list).
- A string containing the known-info about the project (starting as an empty template).

OUTPUT:
- A list of all files inside the given repository (same list from the input for hallucination prevention).
- A sublist of the previous one containing the most relevant files of the project.
- A list of the already read files (repeating work prevention).

The files listed are then individually parsed and passed to the following agent.

---

### AI Summarizer

Then, the **AI Summarizer** comes into play. It will run for every file selected by the **AI Planner**.

GOAL:
- For every file selected by the **AI Planner**, the **AI Summarizer** gets its text dump and tries to update the known information about the project.

INPUT:
- The known-info template.
- The text dump from the file.

OUTPUT:
- The (possibly) updated known-info template, as it might be reading a file with no relevant info.

After the loop ends, it will be time for the next agent.

---

### AI Writer

The next agent is the **AI Writer**.

GOAL:
- With the known-info most likely completed by now, the **AI Writer** generates a a README.md file using an empty README file template.

INPUT:
- The empty README template.
- The most likely complete known-info template.

OUTPUT:
- String containing the complete README.md file.

When the file is ready, it is time to quality check it.

---

### AI Validator

Finally, the **AI Validator** checks the final file.

GOAL:
- Decide whether the final file is either correct, contains format errors or lacks information about the project.

INPUT:
- The empty README template.
- The final README file.

OUTPUT:
- String containing the one of the following words:
  - Correct -> Ready to convert into a README.md file.
  - Format -> Contains formatting errors and must be sent back to the **AI Writer**.
  - Information -> Lacks information about the project and must be sent back to the **AI Planner**.

To prevent infinite loops, we can set a MAX_ITERATIONS variable to the number of maximum iterations we want our workflow to run.

## Zero-Shot Chain of Thought

To improve the quality of the model outputs and reasoning, Zero-Shot Chain of Thought is implemented in the prompting. However this might get changed into usual guided Chain of Thought.

Here's an example of a piece of the **AI Validator** system prompt:

```
Before generating the output, think step by step and reason everything. First, think through the necessary steps between the <thinking>...</thinking> tags, then provide the output between the <output>...</output> tags. Do not output this preamble, start outputting from here:

<thinking>
[insert here your reasoning step by step in order to accomplish the task]
</thinking>
<output>
[insert the status of the inputted file]
</output>
```

And here's an example of output produced by it:

```
<thinking>
To assess the status of this README file, let's evaluate its completeness and formatting.

The project title and summary are provided, along with the programming language used (Python). The necessary sections, including Overview, Installation, Usage, License, and Contact, are all present and well-structured.

The Installation section provides step-by-step instructions, including the command to install the necessary dependencies and clone the repository.

The Usage section has a clear and concise description of the available functions and their respective examples. However, two out of three examples are mentioned as hypothetical and not properly implemented.

The table of contents is properly formatted and links to the corresponding sections.

The License section mentions that the project is licensed under the terms in the LICENSE file, but does not specify the actual license.

The Contact section provides a clear way for users to reach out to the project owner.

Overall, this README file is close to being complete, but the Usage section and License section lack proper information. Also, remember to ignore the License section when checking for status as they have told us to do so.

Since the formatting and most sections are correct, and there is one major missing information which is Usage, the status should be "Information" because it lacks information on 
the implementation of the provided functions.
</thinking>
<output>
Information
</output>
```

This prompting technique really improved the generated READMEs quality by a lot. However, as said before, guiding this Chain of Thought might get even beter results. 

## Contributing

All kinds of contributions are welcomed! Whether you're fixing bugs, improving documentation, or suggesting new features, your help is appreciated.

To contribute to this project, follow these steps:

### 1. Fork the repository: 

Click on the "Fork" button at the top of the repository page.

### 2. Clone your fork:
```bash
  git clone https://github.com/your-username/project-name.git
  ```
### 3. Make the changes:

Ensure to document and explain the change.

### 4. Push the changes:
```bash
  git push origin you-branch-name
  ```

To check-out in what branch your currently working: 
```bash
  git branch
  ```

### 5. Submit a Pull Request:

Go to the original repository and open a pull request so I can add the changes!

## License
This project is licensed under the [MIT License](https://github.com/diegovelilla/AutoREADME/blob/main/LICENSE). See the [LICENSE](https://github.com/diegovelilla/AutoREADME/blob/main/LICENSE) file for more details.

## Contact
For any questions or feedback please reach out to:

- **Email**: [diegovelillarecio@gmail.com](mailto:diegovelillarecio@gmail.com)
- **GitHub Profile**: [diegovelilla](https://github.com/diegovelilla)
- **LinkedIn**: [diego-velilla-recio](https://www.linkedin.com/in/diego-velilla-recio/)

Feel free to open an issue on GitHub or contact me in any way if you have any queries or suggestions.
