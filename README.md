# AutoREADME: Automatize Project Documentation
## Index
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [License](#license)
5. [Contact](#contact)

## Overview
AutoREADME is a GitHub repository analyzer that generates a README file for any given repository. It utilizes the LLaMA 3.1 70B model to gather info from the repository and generate the README file. This project streamlines the documentation process by automating the generation of README files, saving developers time and effort.

## Installation
To install AutoREADME and its dependencies, run the following commands:
```bash
git clone https://github.com/diegovelilla/AutoREADME.git
cd AutoREADME
pip install -r requirements.txt
```
Make sure to change the following line in the config/.env file:
```
GROQ_API_KEY="your_api_key_here"
```
## Usage:
To use AutoREADME, simply substitute the URL in main.py with the URL of the wanted repo:

```python
repo_url="https://github.com/username/repo_name.git"
```

And run this command:

```bash
python3 main.py
```

## License
This project is licensed under the [MIT License](https://github.com/diegovelilla/AutoREADME/blob/main/LICENSE). See the [LICENSE](https://github.com/diegovelilla/AutoREADME/blob/main/LICENSE) file for more details.

## Contact
For any questions or feedback please reach out to:

- **Email**: [diegovelillarecio@gmail.com](mailto:diegovelillarecio@gmail.com)
- **GitHub Profile**: [diegovelilla](https://github.com/diegovelilla)
- **LinkedIn**: [diego-velilla-recio](https://www.linkedin.com/in/diego-velilla-recio/)

Feel free to open an issue on GitHub or contact me in any way if you have any queries or suggestions.
