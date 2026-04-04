import os
from pipelines.find_dog_pipeline import find_dog_pipeline
from zenml.client import Client
 
 
def run_search(image_path: str):
 
    find_dog_pipeline.with_options(enable_cache=False)(image_path=image_path)
 
    try:
        pipeline_model = Client().get_pipeline("find_dog_pipeline")
        last_run = pipeline_model.runs[0]
        result = last_run.steps["response_step"].output.load()

        print(f"{result.get('ids')}")
        print(f"{result.get('confidence')}")
    except Exception as e:
        print(f"{e}")
 
 
if __name__ == "__main__":
    run_search("cat.4986.jpg")