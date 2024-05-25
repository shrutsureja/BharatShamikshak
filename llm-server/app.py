import getpass
import os
import threading

# from flask import Flask
from pyngrok import ngrok, conf


from ragFunction import rag as rag_function
# from GenerateQuestion import generateQuestion
from load_document import ingestDocument
from chatLLM import chat as chat_function

# from flask_ngrok import run_with_ngrok
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS

print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/get-started/your-authtoken")
conf.get_default().auth_token = "2Xo95qEEnLKPCHKPwlp7fUixtfb_3xYRevaXWt33GfP9NnKZW"
app = Flask(__name__)
# run_with_ngrok(app)
CORS(app)

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(5000).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, 5000))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url

# ... Update inbound traffic via APIs to use the public-facing ngrok URL



@app.route('/')
def text():
  return f"Running Flask on Google Colab"

@app.route('/hello', methods=['POST'])
def asd():
  if request.method == 'POST':
    return f"Shrut Sureja"
  else:
    return f"alpa sureja"

@app.route('/ingest', methods=['GET','POST'])
def ingest():

  # headers = {'Content-Type': 'application/json'}
  # data = request.get_json()
  # print(data)
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
  
@app.route('/rag', methods=['GET', 'POST'])
def rag():
  if request.method == 'GET':
    query = request.args.get('query')
    if query is None:
      return jsonify({'error': 'Missing query parameter'}), 400
  else:  # Handle POST request as before (assuming JSON data)
    headers = {'Content-Type': 'application/json'}
    if request.is_json:
      data = request.get_json()
      query = data.get('query')
      if query is None:
        return jsonify({'error': 'Missing query in JSON data'}), 400

  ans, docs, time = rag_function(query)
  print("Answer is : ", ans)
  print("Source Document is : ", docs)
  print("Time taken is : ", time)

  response = {'answer': ans, "source" : docs, "time" : time}
  return jsonify(response)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
  if request.method == 'GET':
    query = request.args.get('query')
    if query is None:
      return jsonify({'error': 'Missing query parameter'}), 400  # Handle missing query
  else:
    headers = {'Content-Type': 'application/json'}
    if request.is_json:
      data = request.get_json()
      query = data.get('query')
      if query is None:
        return jsonify({'error': 'Missing query in JSON data'}), 400  # Handle missing query in JSON
    else:
      return jsonify({'error': 'Request must be JSON'}), 400  # Handle non-JSON requests

  ans, time = chat_function(query)
  print("Answer is : ", ans)
  print("Time taken is : ", time)

  response = {'answer': ans, "time" : time}
  return jsonify(response)

# app.run()
# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()