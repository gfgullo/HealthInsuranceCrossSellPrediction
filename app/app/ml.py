import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model as load_tf_model
from joblib import load
from flask import current_app
from os.path import exists
import csv

np.set_printoptions(suppress=True)

def store_predictions(data, columns=[]):

    fpath = current_app.root_path + "/predictions/data.csv"
    if (exists(fpath)):
        f = open(fpath, "a")
    else:
        f = open(fpath, "w")
        if(columns!=[]):
            f.write(",".join(columns) + "\n")

    data_writer = csv.writer(f, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    data_list = data.astype(str).tolist()

    for sample in data_list:
        data_writer.writerow(sample)
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
    model = load_tf_model(current_app.root_path+"/model/model.h5")
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
