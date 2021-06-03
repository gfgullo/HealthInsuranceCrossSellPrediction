import os
import sagemaker
from sagemaker import get_execution_role
from sagemaker.tensorflow import TensorFlow
import boto3
from botocore.exceptions import ClientError
from datetime import datetime as dt
import tarfile
from os import remove, getcwd
from shutil import move, rmtree
from os.path import abspath
import sys

AWS_ROLE = "role_sagemaker"

DATA_BUCKET = "health-insurance-cross-sell"
DATA_URI = "s3://"+DATA_BUCKET

APP_DIR = abspath("../app/app")
ARCHIVE_NAME = "model.tar.gz"

def upload_data():
    today = dt.now()
    folder = today.strftime("%Y-%m-%d")

    s3 = boto3.client('s3')

    with open(APP_DIR+"/predictions/data.csv", "rb") as f:
        s3.upload_fileobj(f, DATA_BUCKET, folder+"/data.csv")

    with open(APP_DIR+"/model/model.h5", "rb") as f:
        s3.upload_fileobj(f, DATA_BUCKET, folder+"/model.h5")


def download_model(model_dir):
    p = model_dir.split("/")
    bucket_name, bucket_path = p[2], p[3]
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(bucket_path+"/output/"+ARCHIVE_NAME, ARCHIVE_NAME)

    
def extract_move_delete(archive_name):
    archive_path = abspath(archive_name)
    tar = tarfile.open(archive_path, "r:gz")
    tar.extractall()
    tar.close()
    move(archive_path, APP_DIR+"/model/"+archive_name)
    rmtree("00000001")
    

def write_log():
    f = open("learning.log", "a+")
    f.write("COMPLETED\n")
    f.close()

    
if __name__== "__main__":
    
    print(getcwd())
    print(sys.path[0])
    print("Uploading collected samples on S3...", end="")
    training_data_uri = upload_data()
    print("DONE")
    
    sagemaker_session = sagemaker.Session()

    role = "role_sagemaker"
    region = sagemaker_session.boto_session.region_name
    
    print("Starting online learning...")
    
    """
    estimator = TensorFlow(
    entry_point="training_script.py",
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
    """
    
    write_log()
    print("\nCOMPLETED!\n")
        
    