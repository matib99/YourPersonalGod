from llama_cpp import Llama
import json
import copy
import sys


llama = Llama(model_path = "../../models/ggml-vicuna-13B-1.1-q4_0.bin", seed=0, use_mlock=True, n_ctx=2**12, )

#(model_path, n_ctx=512, n_parts=-1, n_gpu_layers=0, seed=1337, f16_kv=True, logits_all=False, vocab_only=False, use_mmap=True, use_mlock=False, embedding=False, n_threads=None, n_batch=512, last_n_tokens_size=64, lora_base=None, lora_path=None, verbose=True)


#(model_path, n_ctx=512, n_parts=-1, n_gpu_layers=0, seed=1337, f16_kv=True, logits_all=False, vocab_only=False, use_mmap=True, use_mlock=False, embedding=False, n_threads=None, n_batch=512, last_n_tokens_size=64, lora_base=None, lora_path=None, verbose=True)

print("model loaded")

def generate_prompt(input_text, file_path, replacements):
    with open(file_path, 'r') as file:
        text = file.read()

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text + str(input_text) + "\nAI : "

replacements = {
    '[[USER_NAME]]': 'Human',
    '[[AI_NAME]]': 'AI'
}
"""
# Specify the file path
file_path = './prompt.txt'
inputtext = str(input("input prompt: "))
preprompt = generate_prompt(inputtext, file_path, replacements)
#print(preprompt)
output = llama(preprompt, max_tokens = 50, stop = ["\n", "Question:", "Q:"], echo = True, suffix="\n")
print(json.dumps(output, indent = 2))
ans = copy.deepcopy(output)["choices"][0]["text"]
print(ans.replace(preprompt, ""))
"""
prompt = input("give prompt: ")
stream = llama(prompt, max_tokens = 2000, stop = ["Question:", "Q:"], stream = True)
fulltext=""
for output in stream:
    fragment = copy.deepcopy(output)
    print(fragment["choices"][0]["text"])
    fulltext+=fragment["choices"][0]["text"]
print(fulltext)
