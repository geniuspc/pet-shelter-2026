import numpy as np
from zenml import step 

@step 
def response_step(ids : str , confidence : str ,  is_valid : bool) -> dict :

     if(is_valid):
         return {"ids" : ids,
                  "confidence" : [confidence]}