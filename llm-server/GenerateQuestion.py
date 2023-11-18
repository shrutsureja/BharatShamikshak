import logging
import sys
import pandas as pd
import os
from llmload import LoadLLM
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.evaluation import DatasetGenerator, RelevancyEvaluator
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    LLMPredictor,
    Response,
)
source_directory = os.environ.get('SOURCE_DIRECTORY', 'source_documents')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = os.environ.get('MODEL_N_BATCH')

def generateQuestion():    
    reader = SimpleDirectoryReader(source_directory)
    documents = reader.load_data()

    data_generator = DatasetGenerator.from_documents(documents)

    eval_questions = data_generator.generate_questions_from_nodes()

    print(eval_questions)


# define jupyter display function
def display_eval_df(query: str, response: Response, eval_result: str) -> None:
    eval_df = pd.DataFrame(
        {
            "Query": query,
            "Response": str(response),
            "Source": (
                response.source_nodes[0].node.get_content()[:1000] + "..."
            ),
            "Evaluation Result": eval_result,
        },
        index=[0],
    )
    eval_df = eval_df.style.set_properties(
        **{
            "inline-size": "600px",
            "overflow-wrap": "break-word",
        },
        subset=["Response", "Source"]
    )
    print(eval_df)

def generateQuestionEval():    
    reader = SimpleDirectoryReader(source_directory)
    documents = reader.load_data()

    data_generator = DatasetGenerator.from_documents(documents)

    eval_questions = data_generator.generate_questions_from_nodes()

    print(eval_questions)

    service_context_gpt4 = ServiceContext.from_defaults(llm=LoadLLM(n_ctx=model_n_ctx, n_batch=model_n_batch, verbose=False))
    evaluator_gpt4 = RelevancyEvaluator(service_context=service_context_gpt4)

    vector_index = VectorStoreIndex.from_documents(
        documents, service_context=service_context_gpt4
    )
    query_engine = vector_index.as_query_engine()
    response_vector = query_engine.query(eval_questions[1])
    eval_result = evaluator_gpt4.evaluate_response(
        query=eval_questions[1], response=response_vector
    )
    display_eval_df(eval_questions[1], response_vector, eval_result)
