import os

from flask import Flask
import yaml


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.yaml"), "r") as config_file:
    config = yaml.safe_load(config_file)

app = Flask(__name__)
app.secret_key = config["flask"]["secret_key"]
import routes
