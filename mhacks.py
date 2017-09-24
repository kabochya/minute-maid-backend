from flask import Flask
from flask import request
import os
from config import app_config
from flask_cloudy import Storage
from transcribe import *
import json

# Using ENV to specify the configuration file
# dev: development mode
# prod: production mode

app = Flask(__name__)
config_name = os.getenv('ENV')
app.config.from_object(app_config[config_name])

app.config.update({
    "STORAGE_PROVIDER": "GOOGLE_STORAGE", # Can also be S3, GOOGLE_STORAGE, etc...
    "STORAGE_KEY": "",
    "STORAGE_SECRET": "",
    "STORAGE_CONTAINER": "./",  # a directory path for local, bucket name of cloud
    "STORAGE_SERVER": True,
    "STORAGE_SERVER_URL": "/files" # The url endpoint to access files on LOCAL provider
})

# Setup storage
storage = Storage()
storage.init_app(app)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/file-ready", methods=['POST'])
def process_audio_file():
    if request.method == "POST":
        data = request.data
        data_json = json.loads(data)
        file_id = data_json.get("file_id")
        if file_id:
            return json.dumps(request.json)
            # download from gcp
            data = download_from_GCP(file_id)
            # analysing audio file
            sentences = get_sentences(data)
            # cluster and summarize
            # save result in db

            # return result back


def download_from_GCP(file_name):
    client = storage.Client(project=app.config["PROJECT_ID"])
    bucket = client.bucket(app_config["BUCKET_ID"])
    blob = bucket.get_blob(file_name)
    if blob:
        return blob.download_as_string()
    else:
        print("File %s not found" % file_name)
