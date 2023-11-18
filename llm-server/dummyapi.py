from ragFunction import rag
# from GenerateQuestion import generateQuestion
from load_document import ingestDocument
from chatLLM import chat

while True:
    stage = input("\nEnter a stage: ")
    if stage == "ingest":
        print("Ingesting...")
        #not to be used still underdevlopment
        # can generate a request though to ingest the document 
        ingestDocument()
    elif stage == "question":
        print("Generating question...")
        print("Under Development...")
        # generateQuestion()#not to be used still underdevlopment
    elif stage == "rag":
        print("Ask the Question...")
        while True:
            query = input("\nEnter a question: ")
            if query == "exit":
                print("Exiting... RAG")
                break
            else:
                ans, docs, time = rag(query)## ans will have the answer and docs will have the source document time is the time taken to answer
                print("Answer is : ", ans)
                print("Source Document is : ", docs)
                print("Time taken is : ", time)
    elif stage == "chat":
        print("Chat with LLM...")
        while True:
            query = input("\nEnter a question: ")
            if query == "exit":
                print("Exiting... Chat")
                break
            else:
                ans, time = chat(query)## ans will have the answer and time is the time taken to answer
                print("Answer is : ", ans)
                print("Time taken is : ", time)
    elif stage == "exit":
        break
    else:
        print("Invalid stage")