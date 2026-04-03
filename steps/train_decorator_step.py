from zenml import step 
from sklearn.ensemble import IsolationForest
import numpy as np

@step
def train_decorator_step(embedings : np.ndarray):

    model = IsolationForest(n_estimators=100 , contamination = 0.05 , random_state = 42)

    model.fit(embedings)

    return model