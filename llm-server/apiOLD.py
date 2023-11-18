#!/usr/bin/env python3
from constants import CHROMA_SETTINGS
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import os
import argparse
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))

# Parse the command line arguments
# args = parse_arguments()
embeddings = HuggingFaceInstructEmbeddings(model_name=embeddings_model_name)
chroma_client = chromadb.PersistentClient(
    settings=CHROMA_SETTINGS, path=persist_directory)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS, client=chroma_client)
retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
# activate/deactivate the streaming StdOut callback for LLMs
# callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
# Prepare the LLM
match model_type:
    case "LlamaCpp":
        llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx,
                       n_batch=model_n_batch, verbose=False)
    case "GPT4All":
        llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj',
                      n_batch=model_n_batch, callbacks=callbacks, verbose=False)
    case _default:
        # raise exception if model_type is not supported
        raise Exception(
            f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")

qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

print("qa-done")

@app.route('/api', methods=['POST'])
def receive_data():
    headers = {'Content-Type': 'application/json'}
    data = request.get_json()
    print(data)
    query = data['question']
    print(query)


    start = time.time()
    res = qa(query)
    answer, docs = res['result'],res['source_documents']
    end = time.time()

    # Print the result
    print("\n\n> Question:")
    print(query)
    print(f"\n> Answer (took {round(end - start, 2)} s.):")
    print(answer)

    # Print the relevant sources used for the answer
    for document in docs:
        print("\n> " + document.metadata["source"] + ":")
        print(document.page_content)
        break
    
    response = {'message': answer,'resource':document.page_content}
    return jsonify(response)


def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)   


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5005)
