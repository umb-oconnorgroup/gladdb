import os

from flask import render_template, send_file
import pandas as pd
import json
import plotly
import plotly.express as px

from app import app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visualize")
def visualize():
    df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/plotable.csv"), index_col=0)
    fig = px.scatter(df, x='PC 1', y='PC 2', color="Dataset", symbol=None, hover_name=df.index, hover_data=['Population', 'Country', 'State', 'City', 'Sex', 'Ethnicity'], render_mode='webgl')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("visualize.html", graphJSON=graphJSON)

@app.route("/match")
def match():
    return render_template("match.html")

@app.route("/download-principal-components")
def download_principal_components():
    principal_components_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.principal_components.npy")
    return send_file(principal_components_path, attachment_filename="glad_principal_components.npy", as_attachment=True)
