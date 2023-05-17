from flask import Flask, request
from Conversation.conversation import Conversation


app = Flask(__name__)

@app.route("/test", methods=["POST"])
def process():
    text = request.form["prompt"]
    answer = conversation.respond(text)
    return answer


if __name__ == '__main__':
    conversation = Conversation(initial_prompt = "Question: What is the Final Shape? Answer: The Final Shape is that which remains when all that can be removed, has been removed.",
                                 model_path = "Conversation\\ggml-old-vic13b-q4_0.bin")
    app.run()
