# from llmload import LoadLLM
from embeddingsload import LoadEmbeddings

from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import LlamaCpp
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
model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))
model_path = os.environ.get('MODEL_PATH')

from constants import CHROMA_SETTINGS
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

def rag(query: str) -> str:
    """
    Function to perform retrieval-based question answering using RAG (Retrieval-Augmented Generation).

    Args:
        query (str): The input question/query.

    Returns:
        str: The generated answer to the question.
    """
    # Load embeddings
    embed = LoadEmbeddings()

    # Initialize Chroma client
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)

    # Initialize Chroma vector store
    db = Chroma(persist_directory=persist_directory, embedding_function=embed, client_settings=CHROMA_SETTINGS, client=chroma_client)

    # Create retriever using Chroma vector store
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

    # Activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [StreamingStdOutCallbackHandler()]

    # Initialize LLM based on device type
    match device_type:
        case "CPU":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False)
        case "GPU":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False, n_gpu_layers=90)
        case _default:
            # Raise exception if device type is not supported
            raise Exception(f"Device type {device_type} is not supported. Please choose one of the following: CPU, GPU")

    # Create RetrievalQA instance using LLM and retriever
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    # Perform question answering
    start = time.time()
    res = qa(query)
    answer = res['result']
    docs = res['source_documents']
    end = time.time()

    # Print the question and answer
    print("\n> Question: " + query)
    print(f"\n> Answer: (took {round(end - start, 2)} s.)\n" + answer)

    # Print the length of the answer
    print("Answer length is:", len(answer))

    # Print the source documents
    print("\n> Source Documents:", docs[0].page_content)

    # TODO: Uncomment the following lines to calculate the similarity score
    # em = embed.encode([answer, docs[0].page_content])
    # score = cos_sim(em[0], em[1])
    # print("\n> " + f"Score: {score}")

    print("RAG COMPLETED")
    return answer, docs[0].page_content, round(end - start, 2)
