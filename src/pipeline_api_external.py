from Conversation.conversation import Conversation
from Conversation.conversation import read_initial_prompt
from flask import Flask, request, jsonify

app = Flask(__name__)
model_path="../models/koala-7B.ggmlv3.q4_0.bin" #path to LLM model (4 bit quantized)
conversation = Conversation(initial_prompt = read_initial_prompt(), model_path = model_path)

@app.route('/api', methods=['POST'])
def print_post_data():
    data = request.get_json()  # get JSON data
    transcription = data["response"]
    response = conversation.respond(transcription, max_tokens=40)
    
    if data and "response" in data and isinstance(data["response"], str):
        print(data["response"])
        return jsonify({'message': response}), 200
    else:
        return jsonify({'error': 'Invalid data, a string was expected'}), 400


if __name__ == '__main__':
    app.run(debug=True)