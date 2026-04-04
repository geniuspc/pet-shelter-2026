from zenml import step
from src.database import db_handler
import numpy as np
import asyncio
 
 
@step
def save_step(ids: str, embeddings: np.ndarray, after_search: float) -> None:

    asyncio.run(db_handler.save_animal(ids, embeddings))
 