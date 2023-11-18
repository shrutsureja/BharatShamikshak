from llmload import LoadLLM
from embeddingsload import LoadEmbeddings

from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
import chromadb

from dotenv import load_dotenv
import os
import time

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

persist_directory = os.environ.get('PERSIST_DIRECTORY')
device_type = os.environ.get('DEVICE_TYPE')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

from constants import CHROMA_SETTINGS
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

def rag(query : str) -> str:
    embed = LoadEmbeddings()
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS , path=persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=embed, client_settings=CHROMA_SETTINGS, client=chroma_client)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [StreamingStdOutCallbackHandler()]

    match device_type:
        case "CPU":
            llm = LoadLLM(n_ctx=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False)
        case "GPU":
            llm = LoadLLM(n_ctx=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False ,n_gpu_layers = 90)
        case _default:
            # raise exception if model_type is not supported
            raise Exception(f"Divice type {device_type} is not supported. Please choose one of the following: CPU , GPU ")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= True)
    # map reduce to get the best answer
    start = time.time()
    res = qa(query)
    answer = res['result']
    docs = res['source_documents']
    end = time.time()

    print("\n> Question :" + query)
    print(f"\n> Answer : (took {round(end - start,2)} s.)\n" + answer)
    
    
    print("Answer length is : ",len(answer))
    print("\n> Source Documents :",docs[0].page_content)

    #error
    # em = embed.encode([answer,docs[0].page_content])
    # score = cos_sim(em[0], em[1])
    # print("\n> "+f"Score :- {score}")
    print("RAG COMPLETED")
    return answer, docs[0].page_content, round(end - start,2)