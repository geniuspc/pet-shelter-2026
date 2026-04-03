from zenml import step
from database import db_handler
import numpy as np
import asyncio
 
 
@step
def save_step(embeddings: np.ndarray) -> None:
 

    asyncio.run(db_handler.save_animal(embeddings))