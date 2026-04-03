from zenml import step 
from src.database import db_handler
import numpy as np
import asyncio

@step 
def save_step(ids : str , metadata , embeddings):

    return asyncio.run(db_handler.save_dog(
        ids = ids ,
       metadata = metadata ,
      embeddings = embeddings))