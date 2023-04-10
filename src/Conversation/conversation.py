import openai
import dotenv


class Conversation():
    # OpenAI API key is required
    # It could be stored in an .env file
    # Model can be replaced by a fine-tuned model later
    def __init__(self, api_key_path: str, initial_prompt: str, model = "gpt-3.5-turbo"):
        self.api_key = dotenv.dotenv_values(api_key_path)["OPENAI_API_KEY"]
        openai.api_key = self.api_key

        self.model = model
        self.initial_prompt = initial_prompt
        self.messages = [ {"role": "system", "content": initial_prompt}]


    # Returns a response based on prompt
    def respond(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model = self.model, messages = self.messages)
        response = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        return response
    

    # Clears messages
    # That should be enough
    def reset(self):
        self.messages = [ {"role": "system", "content": self.initial_prompt}]
