import openai
import dotenv


class Conversation():
    # Not sure what initial_prompt is supposed to be
    # OpenAI API key is required. It could be stored in an .env file
    # Model can be replaced by a fine-tuned model
    def __init__(self, initial_prompt: str, api_key_path: str, model = "text-davinci-003", temperature = 0.5):
        self.api_key = dotenv.dotenv_values(api_key_path)["OPENAI_API_KEY"]
        self.initial_prompt = initial_prompt 
        self.model = model
        self.temperature = temperature


    # Returns a response based on prompt
    def respond(self, message: str) -> str:
        openai.api_key = self.api_key
        response = openai.Completion.create(model = self.model, prompt = message, )
        return response.choices[0].text
