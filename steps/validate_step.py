from zenml import step 
import numpy as np
from database import db_handler 
import asyncio

@step
def validate_step(embedding : np.ndarray) -> bool:

    return asyncio.run(db_handler.is_valid(embedding))
