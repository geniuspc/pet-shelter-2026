from zenml import step
from sklearn.ensemble import IsolationForest
import numpy as np
 
 
@step
def train_decorator_step(embeddings: np.ndarray) -> IsolationForest:
 
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
 
    model.fit(embeddings.reshape(1, -1) if embeddings.ndim == 1 else embeddings)
 
    return model