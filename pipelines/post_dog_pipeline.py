from zenml import pipeline
from steps.encode_step import encode_step
from steps.save_step import save_step
from steps.train_decorator_step import train_decorator_step
from steps.validate_step import validate_step

@pipeline
def post_dog_pipeline(enable_cache=False , id : str = "0"):

    id += 1

    encoded_emb = encode_step()

    train_decorator_step(encoded_emb)

    is_valid = validate_step(encoded_emb)

    save_step(id)

