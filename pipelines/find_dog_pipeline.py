from zenml import pipeline
from steps.response_step import response_step
from steps.encode_step import encode_step
from steps.search_step import search_step
from steps.train_decorator_step import train_decorator_step
from steps.validate_step import validate_step
 
 
@pipeline
def find_dog_pipeline(image_path: str, enable_cache: bool = False):
 
    encoded_emb = encode_step(image_path=image_path)
 
    train_decorator_step(encoded_emb)
 
    is_valid = validate_step(encoded_emb)
 
    matched_id, confidence = search_step(embedding=encoded_emb)
 
    
    response_step(ids=matched_id, confidence=confidence, is_valid=is_valid)
 