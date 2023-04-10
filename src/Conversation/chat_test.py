from conversation import Conversation
import os


path = os.path.join(os.getcwd(), ".\\Conversation\\.env")
conversation = Conversation(initial_prompt = "You are a helpful and intelligent assistant. Your interlocutor is not. Be ready for anything.", api_key_path = path)

while True:
    prompt = input()
    if prompt == "reset":
        conversation.reset()
        continue

    # You exceed your current quota
    # That's not unexpected, given I have paid nothing
    # Too bad I'm not willing to at the moment
    response = conversation.respond(prompt)
    print(response)
