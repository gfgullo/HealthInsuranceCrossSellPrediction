import pandas as pd
from tensorflow.keras.models import load_model as load_tf_model
from joblib import load


def preprocess(data):    

    df = pd.DataFrame(data, index=[0])
    df["Gender"] = df["Gender"].map({'Male':1, 'Female':0})
    #df["Vehicle_Damage"] = df["Vehicle_Damage"].map({'Yes':1, 'No':0})
    df["Vehicle_Age"] = df["Vehicle_Age"].map({'> 2 Years':2, '1-2 Year':1.5, '< 1 Year':1 })

    x = df.values

    ct = load("model/columns_transformer.joblib")
    ss = load("model/standard_scaler.joblib")
    
    x = ct.transform(x).toarray()
    x = ss.transform(x)

    return x


def load_model():
    model = load_tf_model("model/model_2.h5")
    return model


def predict(data, return_confidence=True):

    x = preprocess(data)
    model = load_model()

    confidence = model.predict(x)[0][0]
    response = int(confidence>0.5)

    if not return_confidence:
        return response

    if response==0:
        confidence = 1.-confidence

    confidence = float(confidence)
    confidence = round(confidence, 2)

    return response, confidence