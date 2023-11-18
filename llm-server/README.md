# LLM server

to clone this repo 

- Create your personal API(classic) token and make sure to name it, check when the token expires and tick the first option []repos.

- git clone https://{API Token}@github.com/shrutsureja/SSIP.git

can run this is 2 ways 
- colab : to run this on colab upload SS_RAG.ipynb in the colab in T4 machine, make sure that you use your own ngrok auth token
- locally :
    - download the model in the a models folder 
    - change the model path in the ex.env according to the model
    - rename the ex.env into .env before using the app
    - run localapp.py 



##Doubts
- once the model is loaded in the machine can we change the model parameters in the 2nd call or not