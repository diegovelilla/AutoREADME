from groq import Groq
from dotenv import dotenv_values

CONFIG = dotenv_values("config/.env")


class groq_model:

    def __init__(self):
        """
        Initializes the model from .env with the given parameters.
        """
        self.client = Groq(api_key=CONFIG["GROQ_API_KEY"])
        self.model_name = CONFIG["MODEL_NAME"]

    def answer(self, system_prompt, prompt, json):
        """
        Generates a response from the model based on the provided prompt.

        Parameters:
        system_prompt (str): The system_prompt that will change how the agent works.
        prompt (str): The user query to generate a response for.

        Returns:
        str: The response from the model as a string formatted as a list.
        """
        if (json):
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"{system_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ],
                model=self.model_name,
                response_format={"type": "json_object"}
            )

            return response.choices[0].message.content
        else:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"{system_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ],
                model=self.model_name,
            )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
