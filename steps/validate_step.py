from zenml import step 
from src.database import db_handler
import numpy as np
import asyncio

@step 
def validate_step(embedding : np.ndarray) -> np.ndarray: 

    return asyncio.run(db_handler.encode_search(embedding))
