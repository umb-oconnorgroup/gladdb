import json
import os
import uuid

from flask import flash, redirect, render_template, request, send_file
import pandas as pd
import json
import plotly
import plotly.express as px
import yaml

from app import app


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.yaml"), "r") as config_file:
    config = yaml.safe_load(config_file)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visualize")
def visualize():
    df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/plotable.csv"), index_col=0)
    fig = px.scatter(df, x='UMAP2d 1', y='UMAP2d 2', color="Cohort", symbol=None, hover_name=df.index, hover_data=['Population', 'Country', 'State', 'City', 'Sex', 'Ethnicity'], render_mode='webgl')
    fig.update_layout(height=800)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("visualize.html", graphJSON=graphJSON)

@app.route("/find-controls", methods=["GET", "POST"])
def find_controls():
    if request.method == "POST":
        if "query-file" not in request.files or len(request.files["query-file"].filename) == 0:
            flash("Select a valid query.npz file")
            return redirect(request.url)
        if "email" not in request.form or len(request.form["email"]) == 0:
            flash("Please enter a valid email address to receive notification of completion")
            return redirect(request.url)
        else:
            task_id = str(uuid.uuid1())
            task_data_dir = config["tasks"]["data_dir"]
            os.makedirs(os.path.join(task_data_dir, task_id))
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
    # principal_components_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/data/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.filtered.pca.npy")
    # return send_file(principal_components_path, attachment_filename="glad_principal_components.npy", as_attachment=True)
    return redirect("https://github.com/umb-oconnorgroup/gladprep")
