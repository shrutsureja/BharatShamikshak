#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from langchain.document_loaders import PyPDFLoader
# Loaders
from langchain.schema import Document

# Splitters
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Embedding Support
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings

# Summarizer we'll use for Map Reduce
from langchain.chains.summarize import load_summarize_chain

# Data Science
import numpy as np
# from sklearn.cluster import KMeans

from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain,StuffDocumentsChain
from langchain.chains.mapreduce import MapReduceChain


import os
import argparse
import time
import textract

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))




def main():
    # activate/deactivate the streaming StdOut callback for LLMs
    
    # Prepare the LLM
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path,max_tokens=4096,verbose=False)
        case "GPT4All":
            llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj', n_batch=model_n_batch, callbacks=callbacks, verbose=False)
        case _default:
            # raise exception if model_type is not supported
            raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")
    # Load the book
    loader = PyPDFLoader("./source/Guidelines.pdf")
    pages = loader.load()

    # Cut out the open and closing parts
    # pages = pages[26:277]

    # Combine the pages, and replace the tabs with spaces
    text = ""

    for page in pages:
        text += page.page_content
        
    text = text.replace('\t', ' ')   

    num_tokens = llm.get_num_tokens(text)

    print (f"This Document has {num_tokens} tokens in it")

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=500, chunk_overlap=100)

    docs = text_splitter.create_documents([text])

    num_documents = len(docs)

    print (f"Now our book is split up into {num_documents} {docs[4]}documents")
    
    # Create embeddings
    # embeddings = HuggingFaceInstructEmbeddings(model_name=embeddings_model_name)

    # vectors = embeddings.embed_documents([x.page_content for x in docs])

    # # Map
    # map_template = """The following is a set of documents
    # {docs}
    # Based on this list of docs, please identify the main themes 
    # Helpful Answer:"""
    # map_prompt = PromptTemplate.from_template(map_template)
    # map_chain = LLMChain(llm=llm, prompt=map_prompt)
    # # Reduce
    # reduce_template = """The following is set of summaries:
    # {docs}
    # Take these and distill it into a final, consolidated summary of the main themes. 
    # Helpful Answer:"""
    # reduce_prompt = PromptTemplate.from_template(reduce_template)

    # # Run chain
    # reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    # combine_documents_chain = StuffDocumentsChain(
    #     llm_chain=reduce_chain, document_variable_name="docs"
    # )

    # # Combines and iteravely reduces the mapped documents
    # reduce_documents_chain = ReduceDocumentsChain(
    #     # This is final chain that is called.
    #     combine_documents_chain=combine_documents_chain,
    #     # If documents exceed context for `StuffDocumentsChain`
    #     collapse_documents_chain=combine_documents_chain,
    #     # The maximum number of tokens to group documents into.
    #     token_max=4000,
    # )
    
    # # Combining documents by mapping a chain over them, then combining results
    # map_reduce_chain = MapReduceDocumentsChain(
    #     # Map chain
    #     llm_chain=map_chain,
    #     # Reduce chain
    #     reduce_documents_chain=reduce_documents_chain,
    #     # The variable name in the llm_chain to put the documents in
    #     document_variable_name="docs",
    #     # Return the results of the map steps in the output
    #     return_intermediate_steps=False,
    # )

    # print(map_reduce_chain.run(docs))

    summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce')
    output = summary_chain.run(docs)

    print(output)

if __name__ == "__main__":
    main()
