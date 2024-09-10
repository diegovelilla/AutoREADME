# AutoREADME: Automatize Project Documentation
## Index
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)
6. [Contact](#contact)

---

## Overview
AutoREADME is a GitHub repository analyzer that generates a README file for any given repository. It utilizes the LLaMA 3.1 70B model to gather info from the repository and generate the README file. This project streamlines the documentation process by automating the generation of README files, saving developers time and effort.

## Features
- Clones a repository and generates a tree structure
- Reads system prompts for parser, summarizer, and writer from separate files
- Uses a llama_3_1_70B model to answer system prompts and generate a list of files to check
- Generates a summary for each file using the file contents
- Uses the summaries to generate a README file
- Logs summaries and writes the final README file to the local directory
- Removes the repository after generating the README file

## Installation
To install the AutoREADME project, you will need to:
- Clone the repository using Git
- Install the required dependencies, including the LLaMA 3.1 70B model and GROQ client
- Configure the .env file with your API key and other environment variables

## Usage
To use the AutoREADME project, follow these steps:
- Clone a repository to analyze
- Generate a tree structure of the repository
- Read system prompts for parser, summarizer, and writer from separate files
- Use the llama_3_1_70B model to answer system prompts and generate a list of files to check
- Generate a summary for each file using the file contents
- Use the summaries to generate a README file
- Log summaries and write the final README file to the local directory

## License
This project is licensed under the [MIT License](https://github.com/diegovelilla/AutoREADME/blob/main/LICENSE). See the [LICENSE](https://github.com/diegovelilla/AutoREADME/blob/main/LICENSE) file for more details.

## Contact
For any questions or feedback please reach out to:

- **Email**: [username@gmail.com](mailto:diegovelillarecio@gmail.com)
- **GitHub Profile**: [username](https://github.com/diegovelilla)
- **LinkedIn**: [username](https://www.linkedin.com/in/diego-velilla-recio/)

Feel free to open an issue on GitHub or contact me in any way if you have any queries or suggestions.