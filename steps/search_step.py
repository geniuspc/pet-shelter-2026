from zenml import step 
from src.database import db_handler
import numpy as np
import asyncio

@step 
def search_step(ids : str , embeddings : np.ndarray) -> np.ndarray: 

    return asyncio.run(db_handler.search_dog(
        ids = ids ,
       embeddings = embeddings))
