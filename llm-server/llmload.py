from langchain.llms import LlamaCpp

from dotenv import load_dotenv
import os
import time

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)
    
model_path = os.environ.get('MODEL_PATH')
device_type = os.environ.get('DEVICE_TYPE')
llm = None

def load():
    global llm
    start = time.time()
    print("Loading LLM...")
    if llm is None:
        match device_type:
            case "CPU":
                llm = LlamaCpp(model_path=model_path)
            case "GPU":
                llm = LlamaCpp(model_path=model_path,n_gpu_layers = 90)
            case _default:
                # raise exception if model_type is not supported
                raise Exception(f"Divice type {device_type} is not supported. Please choose one of the following: CPU , GPU ")
    end = time.time()
    print(f"LLM loaded in {round(end - start, 2)} s.")
    print("\nllm : ",llm)
    return "llm loaded"

# def useLLM(**kwargs):
#     if(llm is None):
#         load()
#     start = time.time()
#     print("Using LLM...")
#     llm = llm(**kwargs)
#     end = time.time()
#     print("\nllm : ",llm)
#     return llm