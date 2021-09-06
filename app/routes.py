from flask import render_template

from app import app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/match")
def match():
    return render_template("match.html")
