from llama_cpp import Llama
import json
import copy


llama = Llama(model_path = "./ggml-old-vic13b-q4_0.bin")
print("ok")

prompt = "Question: What is the Final Shape? Answer:"
output = llama(prompt, max_tokens = 100, stop = ["\n", "Question:", "Q:"], echo = True)
print(json.dumps(output, indent = 2))
# print(copy.deepcopy(output)["choices"][0]["text"])
ans = copy.deepcopy(output)["choices"][0]["text"]
print(ans.replace(prompt, ""))


# stream = llama("Question: What is the Final Shape? Answer:", max_tokens = 100, stop = ["\n", "Question:", "Q:"], stream = True)
# for output in stream:
#     fragment = copy.deepcopy(output)
#     print(fragment["choices"][0]["text"])
