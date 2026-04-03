from zenml import pipeline
from steps.response_step import response_step
from steps.encode_step import encode_step
from steps.save_step import save_step
from steps.search_step import search_step
from steps.train_decorator_step import train_decorator_step
from steps.validate_step import validate_step

@pipeline
def find_dog_pipeline(enable_cache = False, confidence : str = "0.8" , run_id: str = "0"):

    encoded_emb = encode_step()

    train_decorator_step(encoded_emb)

    is_valid = validate_step(encoded_emb)

    save_step(embeddings=encoded_emb)

    search_step(embedding=encoded_emb)
    
    conf_score = search_step(embedding=encoded_emb)
    
    conf_str = f"{round(conf_score * 100, 2)}%"

    response_step(ids = run_id , confidence = conf_str, is_valid = is_valid)

