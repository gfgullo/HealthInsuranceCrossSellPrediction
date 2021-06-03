import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from joblib import load
import os
import argparse
import json
from datetime import datetime as dt

def _parse_args():
    parser = argparse.ArgumentParser()

    # Data, model, and output directories
    # model_dir is always passed in from SageMaker. By default this is a S3 path under the default bucket.
    parser.add_argument("--model_dir", type=str)
    parser.add_argument("--sm-model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAINING"))
    parser.add_argument("--hosts", type=list, default=json.loads(os.environ.get("SM_HOSTS")))
    parser.add_argument("--current-host", type=str, default=os.environ.get("SM_CURRENT_HOST"))

    return parser.parse_known_args()


def _preprocess(df, base_dir="/"):    
    df = df.drop(["Probability"], axis=1)
    df["Gender"] = df["Gender"].map({'Male':1, 'Female':0})
    df["Vehicle_Age"] = df["Vehicle_Age"].map({'> 2 Years':2, '1-2 Year':1.5, '< 1 Year':1 })

    x = df.drop(["Prediction"], axis=1).values
    y = df["Prediction"].values

    ct = load(os.path.join(base_dir,"columns_transformer.joblib"))
    ss = load(os.path.join(base_dir, "standard_scaler.joblib"))
    
    x = ct.transform(x).toarray()
    x = ss.transform(x)
   
    return x, y


if __name__ == "__main__":
    
    args, unknown = _parse_args()
    
    today = dt.now()
    folder = today.strftime("%Y-%m-%d")

    data_path = os.path.join(args.train, folder)
    
    df = pd.read_csv(os.path.join(data_path, "data.csv"))
    x, y = _preprocess(df, args.train)
    model = load_model(os.path.join(data_path, "model.h5"), compile=False)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(x, y, epochs=1, batch_size=256, validation_split=0.1)
    
    model.save(os.path.join(args.sm_model_dir, "00000001"))
    model.save(os.path.join(args.sm_model_dir, "model.h5"))