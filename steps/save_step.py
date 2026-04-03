from zenml import step 
from database import db_handler
import numpy as np
import asyncio

@step
def save_step(ids : str) -> np.ndarray:
    
    asyncio.run(db_handler.save_dog(ids))
