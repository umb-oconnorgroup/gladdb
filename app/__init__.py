import os

from flask import Flask


app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = "bigsecret"
from app import routes
