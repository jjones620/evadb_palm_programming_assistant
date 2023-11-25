# CS4420 Programming Assignment 2

## Background
In my first project, I created a basic command line programming assistant using a Huggingface model that was capable of letting users ask questions, but it failed severely for context understanding. This was due to bad embeddings, lack of semantic understanding, and also an inferior model.

## This project
The goal of this project was to improve upon the design of my previous project. I did this in a few ways:

###  LLM choice
For this project, I utilized PaLM 2.0's chat-bison-001. This model proved far superior than the previous model. I used some prompt + context injection for requests to make better when responding to the user.

###  Context
In the previous project, I stored previous user conversations, and tried to check against similarities within the database to use as context. Now, the user has the ability to load files into the database. The files can be of any type. Then, the documents are chunked into 200 character chunks (arbitrary), and semantically compared against user querying through BERT tokenization and embedding. This allows the program to use cosine similarity to compare user queries to chunk's to retrieve the top k most relevant chunks.

### Setup
To run this project, make sure you set up a virtual environment for EvaDB by following the instructions here: https://evadb.readthedocs.io/en/stable/source/overview/getting-started.html
Then, use pip install on the requirements.txt. You will need an API key for PalM 2.0 in your environment variables. You can request one here: https://developers.generativeai.google/tutorials/setup

Now, all you have to do is type "python runner.py" and you can follow the CLI. 

You may have trouble installing transformers, in which case you can try: pip install -U git+https://github.com/huggingface/transformers.git
### Basic demonstration



