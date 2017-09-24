from flask import Flask
from flask import request
import os
from config import app_config
from flask_cloudy import Storage
from transcribe import *
from summarize import summarize
import json

# Using ENV to specify the configuration file
# dev: development mode
# prod: production mode

app = Flask(__name__)
config_name = os.getenv('ENV')
# Get configuration from base config file
app.config.from_object(app_config[config_name])
# Get mongo db
mongo = PyMongo(app)

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
            # download from gcp
            data = download_from_GCP(file_id)
            # analysing audio file
            sentences = get_sentences(data)
            full_text = get_text(sentences)
            # cluster and summarize
            # save result in db
            save_sentences_to_mongo(sentences)
            # return result back
            summarize_sentences = summarize(full_text, 3)
            return json.dump(sentences)


def download_from_GCP(file_name):
    client = storage.Client(project=app.config["PROJECT_ID"])
    bucket = client.bucket(app_config["BUCKET_ID"])
    blob = bucket.get_blob(file_name)
    if blob:
        return blob.download_as_string()
    else:
        print("File %s not found" % file_name)

def save_sentences_to_mongo(file_name, input_sentences):
     sentences = mongo.db.sentences
     sentences.delete_many({"file_name": file_name})
     for s in input_sentences:
        s["file_name"] = file_name
     sentences.insert_many(input_sentences)
