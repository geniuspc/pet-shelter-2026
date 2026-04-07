from typing import Tuple
from zenml import step
import numpy as np
from src.database import db_handler
import asyncio
import nest_asyncio
 
@step
def search_step(embedding: np.ndarray) -> Tuple[str, float]:

    try:

        loop = asyncio.get_running_loop()

    except RuntimeError:

        loop = None

    if loop and loop.is_running():

        nest_asyncio.apply()

        results = asyncio.run(db_handler.search_animal(embedding))

    else:

        results = asyncio.run(db_handler.search_animal(embedding))
 
    
    if not results or not results["ids"] or len(results["ids"][0]) == 0:
        return "Unknown", 0.0
 
    matched_id: str = results["ids"][0][0]
    distance: float = results["distances"][0][0]
 
    confidence = max(0.0, 1.0 - (distance / 2.0))
 
    return matched_id, float(confidence)