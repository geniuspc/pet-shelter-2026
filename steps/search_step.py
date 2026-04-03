from zenml import step 
import numpy as np
from database import db_handler 
import asyncio

@step
def search_step(embedding : np.ndarray, id : str) -> np.ndarray:

    return asyncio.run(db_handler.search_dog(embedding , id))
