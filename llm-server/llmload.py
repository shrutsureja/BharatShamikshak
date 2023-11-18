from langchain.llms import LlamaCpp

from dotenv import load_dotenv
import os
import time

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)
    
model_path = os.environ.get('MODEL_PATH')
llm = None

def LoadLLM(**kwargs):
    global llm
    start = time.time()
    print("Loading LLM...")
    if llm is None:
        llm = LlamaCpp(model_path=model_path, **kwargs)
    end = time.time()
    print(f"LLM loaded in {round(end - start, 2)} s.")
    print("\nllm : ",llm)
    return llm