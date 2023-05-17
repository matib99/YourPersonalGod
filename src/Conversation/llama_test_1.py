from conversation import Conversation


conversation = Conversation(initial_prompt = "Question: What is the Final Shape? Answer: The Final Shape is that which remains when all that can be removed, has been removed.",
                                 model_path = "Conversation\\ggml-old-vic13b-q4_0.bin")
while True:
    print(conversation.respond(input()))
