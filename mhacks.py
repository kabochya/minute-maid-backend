from flask import Flask
from flask import request
import os
from config import app_config
import json

# Using ENV to specify the configuration file
# dev: development mode
# prod: production mode

app = Flask(__name__)
config_name = os.getenv('ENV')
app.config.from_object(app_config[config_name])

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
            # analysing audio file
            # save result in db
            # return result back

