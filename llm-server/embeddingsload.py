from dotenv import load_dotenv

import os 
import time

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")

from langchain.embeddings import HuggingFaceInstructEmbeddings

embed = None

def LoadEmbeddings():
    global embed

    if embed is None:
        strt = time.time()
        print("Loading Embeddings...")
        embed = HuggingFaceInstructEmbeddings(model_name=embeddings_model_name)
        end = time.time()
        print(f"Embeddings loaded in {round(end - strt,2)} s.")
    else:
        print ("Embeddings already loaded")
    print("embed : ",embed)
    return embed