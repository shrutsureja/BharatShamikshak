# from llmload import 
from langchain.llms import LlamaCpp

import time

def chat(query : str):
    # llm = LoadLLM(temperature: 0.8, top_p: 0.95, repeat_penalty: 1.1, top_k: 40, n_ctx: 1024, n_batch: 8, n_gpu_layers: 90, verbose: False)
    llmhere = LlamaCpp(n_ctx=2048, n_batch= 8, max_tokens=512, verbose=False ,n_gpu_layers = 90, temperature=0.5, top_p=0.75, repeat_penalty=1.0, top_k=50)
    start = time.time()
    print("\nLLMhere : ",llmhere)
    # print("\nLLM : ",llm)
    print("\nquery : ",query)
    res = llm(query)
    print("\nresponse :", res)
    end = time.time()
    print(f"\nResponse took : {round(end - start, 2)} s.")
    return res,round(end - start, 2)
