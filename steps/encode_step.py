from zenml import step 
from src.model import ml_handler
import numpy as np
import asyncio

@step
def encode_step(image_path: str) -> np.ndarray:
    
    return ml_handler.encode_image(image_path)
