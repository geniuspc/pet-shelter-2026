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

        self.is_trained = False

    def _load_detector(self , path_to_validator):
        
        if os.path.exists(path_to_validator):

            validator = jl.load(path_to_validator)

            logging.info("Validator was successfuly loaded")

            return validator

        logging.warning("WARN ! Validator wasn`t trained , use fallback training session")

        validator =  IsolationForest(n_estimators = 100 , random_state = 42 , contamination=0.05)

        return validator


    def train_validator(self , embeddings : np.ndarray) :

        model = IsolationForest(n_estimators=100 , contamination = 0.05 , random_state = 42)

        model.fit(embeddings)

        logging.info("Model was successfully trained")

        return model

    def encode_image(self , image) -> np.ndarray:

        emb = self.model.encode(image)

        norm = np.linalg.norm(emb)

        normalized_emb = emb / norm

        return normalized_emb



    def check_is_valid(self , embeddings : np.ndarray , path : str) -> bool :

        validator = self._load_detector(path)

        prediction = validator.predict(embeddings.reshape(1, -1))

        if prediction[0] == 1:
            return True

        return False

ml_handler = MLHandler()