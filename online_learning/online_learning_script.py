import os
import sagemaker
from sagemaker import get_execution_role
from sagemaker.tensorflow import TensorFlow
import boto3
from botocore.exceptions import ClientError
from datetime import datetime as dt
import tarfile
from os import remove
from os.path import exists
from shutil import move, rmtree
import sys
import pandas as pd

MIN_REQUIRED_SAMPLES = 2

AWS_ROLE = "sagemaker_role"

DATA_BUCKET = "health-insurance-cross-sell"
DATA_URI = "s3://"+DATA_BUCKET

LEARNING_PATH = sys.path[0]+"/"
BASE_PATH = LEARNING_PATH.replace("online_learning","")
APP_DIR = BASE_PATH+"app/app/"

SAMPLES_PATH = APP_DIR+"predictions/data.csv"

ARCHIVE_NAME = "model.tar.gz"


def check_data():

    if not exists(SAMPLES_PATH):
        print("Samples file not found !")
        return False

    df = pd.read_csv(SAMPLES_PATH)
    df_count = df.shape[0]

    if df_count<MIN_REQUIRED_SAMPLES:
        print("%d samples collected, minimum required are %d" % (df_count, MIN_REQUIRED_SAMPLES))
        return False

    print("%d samples collected" % df_count)
    return True

def upload_data():
    today = dt.now()
    folder = today.strftime("%Y-%m-%d")

    s3 = boto3.client('s3')

    with open(APP_DIR+"predictions/data.csv", "rb") as f:
        s3.upload_fileobj(f, DATA_BUCKET, folder+"/data.csv")

    with open(APP_DIR+"model/model.h5", "rb") as f:
        s3.upload_fileobj(f, DATA_BUCKET, folder+"/model.h5")


def download_model(model_dir):
    p = model_dir.split("/")
    bucket_name, bucket_path = p[2], p[3]
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(bucket_path+"/output/"+ARCHIVE_NAME, LEARNING_PATH+ARCHIVE_NAME)

    
def extract_move_delete(archive_name):
    archive_path = LEARNING_PATH+archive_name
    tar = tarfile.open(archive_path)
    tar.extractall(path=LEARNING_PATH)
    tar.close()
    move(LEARNING_PATH+"model.h5", APP_DIR+"/model/model.h5")
    remove(archive_path)
    rmtree(LEARNING_PATH+"00000001")
    remove(APP_DIR+"predictions/data.csv")

    
if __name__== "__main__":
    
    if not check_data():
        exit(0)

    print("Uploading collected samples on S3...", end="")
    training_data_uri = upload_data()
    print("DONE")
    
    sagemaker_session = sagemaker.Session()

    role = "role_sagemaker"
    region = sagemaker_session.boto_session.region_name
    
    print("Starting online learning...")
    
    estimator = TensorFlow(
    entry_point=LEARNING_PATH+"training_script.py",
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    framework_version="2.1.0",
    py_version="py3",
    #output_path=training_data_uri
    #wait=False
    )
    
    estimator.fit(DATA_URI)
    
    new_model_dir = estimator.model_dir

    print("Training completed!")
    print("Model stored at: "+new_model_dir)
    
    print("Downloading new model...", end="")
    download_model(new_model_dir)
    print("DONE")
                       
    print("Moving new model inside app...", end="")
    extract_move_delete(ARCHIVE_NAME)
    print("DONE")    