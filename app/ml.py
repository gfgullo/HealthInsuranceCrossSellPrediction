import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model as load_tf_model
from joblib import load
from flask import current_app

def preprocess(data):    

    df = pd.DataFrame(data)
    print(df.head())
    df["Gender"] = df["Gender"].map({'Male':1, 'Female':0})
    #df["Vehicle_Damage"] = df["Vehicle_Damage"].map({'Yes':1, 'No':0})
    df["Vehicle_Age"] = df["Vehicle_Age"].map({'> 2 Years':2, '1-2 Year':1.5, '< 1 Year':1 })

    x = df.values

    ct = load(current_app.root_path+"/model/columns_transformer.joblib")
    ss = load(current_app.root_path+"/model/standard_scaler.joblib")
    
    x = ct.transform(x).toarray()
    x = ss.transform(x)

    return x


def load_model():
    model = load_tf_model(current_app.root_path+"/model/model_2.h5")
    return model


def predict(data, return_confidence=True):

    x = preprocess(data)
    model = load_model()

    confidence = model.predict(x)
    confidence = confidence.ravel()
    
    response = confidence>0.5

    if not return_confidence:
        return response

    confidence = np.where(confidence>0.5, confidence, 1.-confidence)
    confidence = confidence.round(2)

    return response, confidence
