from ragFunction import rag as rag_function
# from GenerateQuestion import generateQuestion
from load_document import ingestDocument
from chatLLM import chat as chat_function

from flask import Flask, render_template,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def text():
  return f"Running Flask on Google Colab"

@app.route('/ingest', methods=['POST'])
def ingest():

  headers = {'Content-Type': 'application/json'}
  data = request.get_json()
  print(data)
  print("Ingesting...")
  #not to be used still underdevlopment
  # can generate a request though to ingest the document 
  ingestDocument()

  response = {'message': "demo result"}
  return jsonify(response)

@app.route('/question', methods=['POST'])
def question():

  headers = {'Content-Type': 'application/json'}
  data = request.get_json()

  print(data)
  print("Generating question...")
  print("Under Development...")
  # generateQuestion()#not to be used still underdevlopment

  response = {'message': "demo result"}
  return jsonify(response)
  
@app.route('/rag', methods=['POST'])
def rag():
  headers = {'Content-Type': 'application/json'}
  data = request.get_json()
  print(data['query'])
   
  ans, docs, time = rag_function(data['query'])## ans will have the answer and docs will have the source document time is the time taken to answer
  print("Answer is : ", ans)
  print("Source Document is : ", docs)
  print("Time taken is : ", time)

  response = {'answer': ans, "source" : docs, "time" : time}
  return jsonify(response)

@app.route('/chat', methods=['POST'])
def chat():

  headers = {'Content-Type': 'application/json'}
  data = request.get_json()
  print(data)
   
  ans, time = chat_function(data['query'])## ans will have the answer and time is the time taken to answer
  print("Answer is : ", ans)
  print("Time taken is : ", time)

  response = {'answer': ans, "time" : time}
  return jsonify(response)

if __name__ == '__main__':
    app.run(port=5001)
