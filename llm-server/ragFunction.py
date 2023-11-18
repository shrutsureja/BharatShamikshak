from llmload import llm
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
    llmhere = llm(model_n_ctx=model_n_ctx, model_n_batch=model_n_batch, callbacks=callbacks)
    qa = RetrievalQA.from_chain_type(llm=llmhere, chain_type="stuff", retriever=retriever, return_source_documents= True)
    print("\nLLMhere : ",llmhere)
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