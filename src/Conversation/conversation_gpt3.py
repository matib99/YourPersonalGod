import openai
import copy

# here prompt should be separeted to following roles:
# system (preamble),
# user (user messages),
# assistant (ai responses)

# element [0] of conversation array will always contain initial prompt

# there is no explicite limit of tokens, one must explain in preamble that they need short answers

class Conversation():
    def __init__(self, session_name: str, initial_prompt: str, model_path = False) -> None:
        self.initial_messages = [{"role": "system", "content": initial_prompt}]
        self.history = self.initial_messages.copy() #unnecesary but may be helpful for debugging purposes
        self.model = "gpt-3.5-turbo-0613"
        self.messages = self.initial_messages.copy()
        self.memory_directory = "./memory"

    def respond(self, message: str, max_tokens=False): #max tokens only so that all classes use simmilar paterns
        self.messages.append(message)
        try:
            response = openai.ChatCompletion.create(
                model = self.model,
                messages = self.messages
            )
            response = response
            response_message = list(response.choices)[0]
            response_message = response_message.to_dict()['message'].to_dict()

        except Exception as e:
            print("Exception occured while generating response: " + str(e))
            response = {"error": str(e)}
            response_message = "Server not responding"

        self.messages.append(response_message)
        print(f"Response from within machine: \t{self.messages[-1]['content']}")
        self.history.append(message)
        self.history.append(response)
        if len(self.messages)>= 15:
            self.messages.pop(1) # user
            self.messages.pop(2) # machine
        return self.history[-1]["choices"][0]["message"]["content"]


    def reset(self) -> None:
        self.messages = self.initial_messages

    def save_memory(self) -> None: #for debugging purposes
        with open(f"{self.memory_directory}{self.session_name}-history.txt", 'w') as f:
            json.dump(self.history, f)
        with open(f"{self.memory_directory}{self.session_name}-messages.txt", 'w') as f:
            json.dump(self.messages, f)

    def read_initial_prompt(self, prompt_path) -> None: #doesn't affect user and assistant messages
        with open(prompt_path, 'r') as f:
            self.initial_prompt = f.read()
            self.initial_messages[0]["content"] = self.initial_prompt
            self.messages[0]["content"] = self.initial_prompt

    def get_response(self) -> str: #fore debugging purposes
        return self.history[-1]["choices"][0]["message"]["content"]
