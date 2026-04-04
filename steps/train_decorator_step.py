import joblib
import os
from zenml import step
from sklearn.ensemble import IsolationForest
import numpy as np

VALIDATOR_PATH = "./models/isolation_forest.joblib"

@step
def train_decorator_step(embeddings: np.ndarray):
    
    os.makedirs(os.path.dirname(VALIDATOR_PATH), exist_ok=True)
    
    model = IsolationForest(contamination=0.1)
    model.fit(embeddings.reshape(1, -1))
    
   
    joblib.dump(model, VALIDATOR_PATH) 
    print(f"Validator trained and saved to {VALIDATOR_PATH}!")