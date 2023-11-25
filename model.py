import google.generativeai as palm
import os
from prompts import AGENT_PROMPT
import evadb
import pprint
import numpy as np
from transformers import BertModel, BertConfig, BertTokenizer

class Model():
    def __init__(self, temperature=0.5):
        api_key = os.environ['API_KEY_PALM']
        
        self.chunk_table = "ChunkTable"  # new table for storing chunks
        self.palm = palm
        self.primary_key = -1
        self.cursor=evadb.connect().cursor()
        self.palm.configure(api_key=api_key)
        self.temperature = temperature

        self.chunk_size = 400
        self.setup_database()

    def ask_question(self, query):

        context = self.get_context(query)

        return self.palm.generate_text(prompt=(AGENT_PROMPT.format(context, query)), 
                                        temperature=self.temperature).result
    def get_context(self, query):
        # i want to retrieve the top 5 most similar chunks
        result = self.cursor.query(f"""SELECT * FROM {self.chunk_table} ORDER BY CosineSimilarityScore(chunk, {"'" + query + "'"}) DESC LIMIT 5;""").df()
        print("context retrieval")
        context =''
        if not result.empty:
            # DataFrame has values
            print("found relevant context")
            for index, row in result.iterrows():
                context += row['chunk']
            
        else:
            # DataFrame is empty
            print("found no relevant context")
            result = self.cursor.query(f"""SELECT * FROM {self.chunk_table} DESC LIMIT 10""").df()
            # if we have results, we want to greedily take context and append it to prompt

            for index, row in result.iterrows():
                context += row['chunk']
        return context
    def setup_tables(self):
        print(self.cursor.query(f"""DROP TABLE {self.chunk_table};""").df())

        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.chunk_table} 
                                 (id INTEGER PRIMARY KEY, 
                                  chunk TEXT
                                   );"""

        print(self.cursor.query(create_table_query).df())

    def save(self, piece):
        insert_query = f"""INSERT INTO {self.chunk_table} (id, chunk) 
                          VALUES ({self.primary_key + 1}, {"'" + piece + "'"});"""
        result = self.cursor.query(insert_query).df()

    def read_in_chunks(self, file_object):
        while True:
            data = file_object.read(self.chunk_size)
            if not data:
                break
            yield data


    def read_file(self, filename):
        full_path = os.path.join(os.getcwd(), filename)
        with open(full_path, 'r') as f:
            for piece in self.read_in_chunks(f):

                self.save(piece)
    


    def setup_function(self):
        create_function_query = f"""CREATE OR REPLACE FUNCTION CosineSimilarityScore

                IMPL  './semantic-comparison.py';
                """
        result = self.cursor.query(create_function_query).df()

    def setup_database(self):
        self.setup_tables()
        self.setup_function()


        