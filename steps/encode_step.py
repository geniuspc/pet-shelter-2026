from zenml import step 
from model import ml_handler
import numpy as np
import asyncio

@step
def encode_step(image_path = "./temp/file_test.jpg") -> np.ndarray:
    
    asyncio.run(ml_handler.encode_image(image_path))
