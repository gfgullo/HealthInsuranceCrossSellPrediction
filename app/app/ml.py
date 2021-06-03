import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model as load_tf_model
from joblib import load
from flask import current_app
from os.path import exists


def store_predictions(data, columns=None):

    np.set_printoptions(suppress=True)

    fpath = current_app.root_path + "/predictions/data.csv"
    if (exists(fpath)):
        f = open(current_app.root_path + "/predictions/data.csv", "a")
    else:
        f = open(current_app.root_path + "/predictions/data.csv", "w")
        if(columns!=None):
            f.write(",".join(columns) + "\n")

    f.write(np.array_str(data)[2:-2]
            .replace("\n", "")
            .replace("  ", " ")
            .replace(" ", ",")
            + "\n")
    f.close()


def preprocess(df):

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

    df = pd.DataFrame(data)
    x = preprocess(df.copy())
    model = load_model()

    confidence = model.predict(x)
    confidence = confidence.ravel()
    confidence = confidence.round(2)

    response = confidence>0.5

    high_confidence_index = confidence>0.95 or confidence<0.05
    df["Prediction"] = response
    df["Probability"] = confidence
    to_write = df.values[high_confidence_index]

    if(to_write.shape[0]>0):
        store_predictions(to_write, columns=df.columns.values)

    if not return_confidence:
        return response

    confidence = np.where(confidence>0.5, confidence, 1.-confidence)

    return response, confidence
