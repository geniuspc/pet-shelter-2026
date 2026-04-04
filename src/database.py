import chromadb as cd
from sklearn.ensemble import IsolationForest
import joblib as jl
import os
import logging
import numpy as np
import asyncio
 
 
class DBHandler():
 
    def __init__(self):
        self.client = cd.PersistentClient(path="./chromadb")
        self.collection = self.client.get_or_create_collection(

            "vector_database_animals",

            metadata={"hnsw:space": "cosine"}
        )
 
    async def save_animal(self, ids: str, embeddings: np.ndarray):

        loop = asyncio.get_running_loop()
 
        existing = await loop.run_in_executor(

            None, lambda: self.collection.get(ids=[ids])

        )

        if existing["ids"]:

            await loop.run_in_executor(

                None, lambda: self.collection.delete(ids=[ids])

            )

            logging.warning(f"Duplicate ID '{ids}' found — replaced with new embedding.")
 
        await loop.run_in_executor(None, lambda: self.collection.add(

            ids=[ids],

            embeddings=[embeddings.tolist()],

        ))

        logging.info(f"Animal '{ids}' saved to vector DB.")
 
    async def search_animal(self, embeddings: np.ndarray) -> dict:

        loop = asyncio.get_running_loop()

        results = await loop.run_in_executor(None, lambda: self.collection.query(

            query_embeddings=[embeddings.tolist()],

            n_results=1

        ))

        return results
 
    async def delete_animal(self, ids: str):

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, lambda: self.collection.delete(ids=ids))

        logging.info(f"Animal '{ids}' deleted successfully.")

    def count(self) -> int:

        return self.collection.count()
 
 
db_handler = DBHandler()