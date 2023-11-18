# LLM server

## Cloning the Repository

To clone this repository, follow these steps:

1. Create your personal API (classic) token on GitHub. Make sure to name it and check when the token expires. Tick the first option "repos" to grant access to repositories.

2. Open your terminal and run the following command:

    ```bash
    git clone https://{API Token}@github.com/shrutsureja/BharatShamikshak.git
    ```

## Running the Server

You can run the server in two ways: locally or on Colab.

### Running Locally

To run the server locally, follow these steps:

1. Download the model and place it in the "models" folder.

2. Open the `ex.env` file and change the model path according to the downloaded model.

3. Rename the `ex.env` file to `.env` before using the app.

4. Run the `localapp.py` file.

### Running on Colab

To run the server on Colab, follow these steps:

1. Upload the `SS_RAG.ipynb` file to Colab.

2. Make sure to use your own ngrok auth token.
