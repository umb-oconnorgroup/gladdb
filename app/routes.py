import os

from flask import flash, redirect, render_template, request, send_file
import pandas as pd
import json
import plotly
import plotly.express as px

from app import app


@app.route("/")
def home():
    # os.environ.get('SECRET_KEY')
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
        if "upload-pca" not in request.files or len(request.files["upload-pca"].filename) == 0:
            flash("Select a valid numpy file")
            return redirect(request.url)
        else:
            resp = requests.post("http://localhost:5001/match", data=request.files["upload-pca"])
            return resp.content, 200
    return render_template("find_controls.html")

@app.route("/download-principal-components")
def download_principal_components():
    principal_components_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/data/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.filtered.pca.npy")
    return send_file(principal_components_path, attachment_filename="glad_principal_components.npy", as_attachment=True)
