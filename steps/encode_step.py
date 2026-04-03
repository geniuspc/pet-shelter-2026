from zenml import step 
from src.model import encode_image
import numpy as np

@step 
def encode_step(image) -> np.ndarray: 

    results = encode_image(image)

    return results
