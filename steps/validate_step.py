from zenml import step
import numpy as np
from src.model import ml_handler
import asyncio
 
VALIDATOR_PATH = "./models/isolation_forest.joblib"

@step
def validate_step(embedding: np.ndarray) -> bool:
    
    return ml_handler.check_is_valid(embedding, VALIDATOR_PATH)