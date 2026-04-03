from zenml import step
import numpy as np
from database import db_handler
import asyncio
 
 
@step
def search_step(embedding: np.ndarray) -> dict:

    results = asyncio.run(db_handler.search_animal(embedding))

    distance = results['distances'][0][0]

    confidence = max(0, 1 - distance)

    return float(confidence)