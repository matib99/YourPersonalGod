from fastapi import FastAPI
from conversation import Conversation, read_initial_prompt

import copy

app = FastAPI()

conv = None

@app.post("/start")
async def start(init_msg=''):
    conv = Conversation(init_msg)


#function for reading initial prompt from prompt.txt file. [[USER_NAME]] and [[AI_NAME]] strings are changed to interlocutors names (you can change them to better prompt your LLM model)
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
    def __init__(self, initial_prompt: str, model_path: str) -> None:
        self.initial_prompt = initial_prompt
        self.current_prompt = initial_prompt
        self.llama = Llama(model_path = model_path)
        print("Model ready")


    def respond(self, message: str, max_tokens=50) -> str:
        self.current_prompt += "\n### Human: {:}\n### AI: ".format(message)
        output = self.llama(
            self.current_prompt,
            max_tokens = max_tokens, 
            #stop = ["\n", "Question:", "Q:"], 
            stop = ["\n"],
            echo = True)
        ans = copy.deepcopy(output)["choices"][0]["text"]
        print(f'\nGods response : {ans.replace(self.current_prompt, "")}\n')
        return ans.replace(self.current_prompt, "")


    def reset(self) -> None:
        self.current_prompt = self.initial_prompt


