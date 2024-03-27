import json
import os
import uuid

from flask import flash, redirect, render_template, request, send_file
from flask_xcaptcha import XCaptcha
import pandas as pd
import json
import plotly
import plotly.express as px
import yaml

from starter import app


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.yaml"), "r") as config_file:
    config = yaml.safe_load(config_file)

app.config['XCAPTCHA_SITE_KEY'] = config["xcaptcha"]["site_key"]
app.config['XCAPTCHA_SECRET_KEY'] = config["xcaptcha"]["secret_key"]
app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"
xcaptcha = XCaptcha(app=app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visualize/<embedding>")
@app.route("/visualize")
def visualize(embedding="PCA"):
    if embedding not in ["UMAP", "PCA"]:
        embedding = "UMAP"
    df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/plotable.csv"), index_col=0)
    df = df.fillna("Missing")
    fig = px.scatter(df, x=embedding+"1", y=embedding+"2", color="PHS", symbol=None, hover_name=df.index, hover_data=["PHS", "Country", "State", "Sex", "SelfDescribedStatus", "HispanicJustification"], render_mode="webgl")
    fig.update_layout(height=800)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("visualize.html", embedding=embedding, graphJSON=graphJSON)

@app.route("/find-controls", methods=["GET", "POST"])
def find_controls():
    if request.method == "POST":
        if "query-file" not in request.files or len(request.files["query-file"].filename) == 0:
            flash("Select a valid query.npz file")
            return redirect(request.url)
        if "email" not in request.form or len(request.form["email"]) == 0:
            flash("Please enter a valid email address to receive notification of completion")
            return redirect(request.url)
        if not xcaptcha.verify():
            flash("Please complete the captcha")
            return redirect(request.url)
        else:
            task_id = str(uuid.uuid1())
            task_data_dir = config["tasks"]["data_dir"]
            os.makedirs(os.path.join(task_data_dir, task_id))
            # verify that uploaded file does not exceed size limit
            request.files["query-file"].seek(0, 2)
            file_size = request.files["query-file"].tell()
            request.files["query-file"].seek(0)
            if file_size > 1e8:
                flash("Your query.npz file exceeds the 100MB size limit")
                return redirect(request.url)
            request.files["query-file"].save(os.path.join(task_data_dir, task_id, "query.npz"))
            with open(os.path.join(task_data_dir, task_id, "params.json"), "w") as params_file:
                json.dump(request.form, params_file)
            flash("Matching job {} has been submitted. You will receive a notification when the results are available.".format(task_id))
    return render_template("find_controls.html")

@app.route("/tasks/<task_id>", methods=["GET"])
def download_results(task_id):
    task_data_dir = config["tasks"]["data_dir"]
    task_dir = os.path.join(task_data_dir, task_id)
    if "match.vcf" in os.listdir(task_dir):
        return send_file(os.path.join(task_dir, "match.vcf"), attachment_filename="match.vcf", as_attachment=True)
    else:
        "Your results are not currently available."

@app.route("/download-prep")
def download_prep():
    return redirect("https://github.com/umb-oconnorgroup/gladprep")
