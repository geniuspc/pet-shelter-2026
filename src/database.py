import chromadb as cd
from sklearn.ensemble import IsolationForest
import joblib as jl
import os
import logging
import numpy as np
import asyncio
from functools import partial

from steps.encode_step import ml_handler
 
 
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

    async def fill_db(self , dir_fol : str) -> None:

        loop = asyncio.get_running_loop()

        filenames = [f for f in os.listdir(dir_fol) if f.lower().endswith((".jpg" , ".png" , ".jpeg"))]

        if not filenames :

            logging.info("Folder is empty")

            return
            
        for filename in filenames :

            full_path = os.path.join(dir_fol , filename)

            file_id = os.path.splitext(filename)[0]

            try:

                emb = await loop.run_in_executor(None , lambda : ml_handler.encode_image(image=full_path))

                await loop.run_in_executor(None , lambda : self.collection.add( ids = [file_id] , embeddings= [emb.tolist()]))

            except Exception as e :

                logging.info(f"{filename} : {e}")

    def count(self) -> int:

        return self.collection.count()
 
 
db_handler = DBHandler()