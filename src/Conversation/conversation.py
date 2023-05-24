from llama_cpp import Llama
import copy

def read_initial_prompt(file_path="./Conversation/prompt.txt", replacements={
        '[[USER_NAME]]': 'Human',
        '[[AI_NAME]]': 'AI'
    }):
        with open(file_path, 'r') as file:
            text = file.read()

        for placeholder, value in replacements.items():
            text = text.replace(placeholder, value)

        return text 

class Conversation():
    # Initial prompt should be in a "Question: (...)? Answer:" fromat
    def __init__(self, initial_prompt: str, model_path: str) -> None:
        self.initial_prompt = initial_prompt
        self.current_prompt = initial_prompt
        self.llama = Llama(model_path = model_path)
        print("Model ready")


    def respond(self, message: str) -> str:
        self.current_prompt += "\nQuestion: {:} Answer:".format(message)
        output = self.llama(self.current_prompt, max_tokens = 100, stop = ["\n", "Question:", "Q:"], echo = True)
        ans = copy.deepcopy(output)["choices"][0]["text"]
        return ans.replace(self.current_prompt, "")


    def reset(self) -> None:
        self.current_prompt = self.initial_prompt

"""
    def read_initial_prompt(self, input_text, file_path="prompt.txt", replacements={
    '[[USER_NAME]]': 'Human',
    '[[AI_NAME]]': 'AI'
}):
        with open(file_path, 'r') as file:
            text = file.read()

        for placeholder, value in replacements.items():
            text = text.replace(placeholder, value)

        return text + str(input_text) + "\nAI : "
"""