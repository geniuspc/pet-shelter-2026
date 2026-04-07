import os
from pipelines.find_dog_pipeline import find_dog_pipeline
from src.database import db_handler
from zenml.client import Client
import asyncio
 
async def run_search(image_path: str, dir_fol : str):
    #for filling vector db
    #await db_handler.fill_db(dir_fol = dir_fol)
 
    find_dog_pipeline.with_options(enable_cache=False)(image_path=image_path)
 
    try:
        pipeline_model = Client().get_pipeline("find_dog_pipeline")
        last_run = pipeline_model.runs[0]
        result = last_run.steps["response_step"].output.load()

        print(f"{result.get('ids')}")
        print(f"{result.get('confidence')}")
        #print(f"{db_handler.collection.get()}")
    except Exception as e:
        print(f"{e}")
 
 
if __name__ == "__main__":
    asyncio.run(run_search("cat.3.jpg", "./temp"))