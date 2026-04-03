import random
from sentence_transformers import SentenceTransformer
import chromadb as cd
from sklearn.ensemble import IsolationForest
import joblib as jl
import os 
import logging
import numpy as np 

class MLHandler():

    def __init__(self , model_name = "clip-ViT-B-32"):

        self.device = "cpu"

        self.model = SentenceTransformer(model_name = model_name , device= self.device)

        self.client = cd.PersistentClient(path = "./chromadb")

        self.collection = self.client.get_or_create_collection("vector_database_dogs")

        self.is_valid = False

    def _load_detector(self , path_to_validator):
        
        if os.path.exists(path_to_validator):

            validator = jl.load(path_to_validator)

            logging.info("Validator was successfuly loaded")

            return validator

        logging.warning("WARN ! Validator wasn`t trained , use fallback training session")

        validator =  IsolationForest(n_estimators = 100 , random_state = 42 , contamination=0.05)

        return validator

    #in prod
    def train_validator(self) :

        #TODO : train model d
        logging.info("wmwdwdwd")

    def encode_image(self , image) -> np.ndarray:

        emb = self.model.encode(image)

        #TODO : normalize 


    #in prod
    def is_valid(self , embeddings : np.ndarray , path : str) -> bool :

        validator = self._load_detector(path)

        if validator.predict(embeddings[0]) == 1 :

            is_valid = True

        return is_valid

