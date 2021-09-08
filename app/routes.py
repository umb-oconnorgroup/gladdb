import os

from flask import flash, redirect, render_template, request, send_file
import pandas as pd
import json
import plotly
import plotly.express as px
from werkzeug.utils import secure_filename

from app import app


ALLOWED_EXTENSIONS = ["npy"]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    # os.environ.get('SECRET_KEY')
    return render_template("index.html")

@app.route("/visualize")
def visualize():
    df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/plotable.csv"), index_col=0)
    fig = px.scatter(df, x='PC 1', y='PC 2', color="Dataset", symbol=None, hover_name=df.index, hover_data=['Population', 'Country', 'State', 'City', 'Sex', 'Ethnicity'], render_mode='webgl')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("visualize.html", graphJSON=graphJSON)

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        if 'pca-file' not in request.files:
            raise ValueError(str(request))
            # flash('No file part')
            return redirect(request.url)
        file = request.files['pca-file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        return render_template("match.html")
    else:
        return render_template("match.html")

@app.route("/download-principal-components")
def download_principal_components():
    principal_components_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.principal_components.npy")
    return send_file(principal_components_path, attachment_filename="glad_principal_components.npy", as_attachment=True)
