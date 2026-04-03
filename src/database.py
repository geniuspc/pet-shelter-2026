import random
from sentence_transformers import SentenceTransformer
import chromadb as cd
from sklearn.ensemble import IsolationForest
import joblib as jl
import os 
import logging
import numpy as np 
import asyncio 

class DBHandler():

    def __init__(self):

        self.client = cd.PersistentClient(path = "./chromadb")

        self.collection = self.client.get_or_create_collection("vector_database_dogs")  
        
    async def save_dog(self , ids : str , embeddings : np.ndarray):

        loop = asyncio.get_running_loop()

        loop.run_in_executor(None , lambda : self.collection.add(
            
                ids= [ids],
                embeddings=[embeddings.tolist()],
            
            ))

        logging.info("The dog was saved to vector db")

    async def search_dog(self, ids : str , embeddings : np.ndarray) -> np.ndarray:

        loop = asyncio.get_running_loop()

        results = await loop.run_in_executor(None , lambda : self.collection.query(
            ids=ids ,
            query_embeddings = [embeddings] ,
            n_results=5)
        )

        return results

    async def delete_dog(self , ids : str):

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None , lambda : self.collection.delete(
                ids = ids
            ))

        logging.info("The dog was deleted successfully!")

db_handler = DBHandler()