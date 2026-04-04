from typing import Tuple
from zenml import step
import numpy as np
from src.database import db_handler
import asyncio
 
 
@step
def search_step(embedding: np.ndarray) -> Tuple[str, float]:
 
    results = asyncio.run(db_handler.search_animal(embedding))
 
    matched_id: str = results["ids"][0][0]
    distance: float = results["distances"][0][0]
 
    confidence = max(0.0, 1.0 - (distance / 2.0))
 
    return matched_id, float(confidence)