import numpy as np
from zenml import step 

@step
def response_step(ids: str, confidence: float, is_valid: bool) -> dict:
    
    conf_str = f"{round(confidence * 100, 2)}%"
 
    if is_valid:
        return {
            "ids": ids,
            "confidence": conf_str
        }

    return {
        "ids": ids,
        "confidence": conf_str,
        "error": "Animal did not pass validation"
    }