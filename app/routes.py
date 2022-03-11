# import io
import os

import dask.array as da
from flask import flash, redirect, render_template, request, send_file, url_for, Response
import pandas as pd
import json
# import numpy as np
import plotly
import plotly.express as px
import requests
# from scipy.optimize import linear_sum_assignment
# from scipy.spatial.distance import cdist
from werkzeug.utils import secure_filename

from app import app


# pca_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/data/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.filtered.pca.applied_to_all.npy")
# explained_variance_ratio_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/data/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.filtered.explained_variance_ratio.npy")
# zarr_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/data/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.zarr")
# glad_pca = np.load(pca_path)
# explained_variance_ratio = np.load(explained_variance_ratio_path)
# glad_genotypes = da.from_zarr(os.path.join(zarr_path, "call_genotype"))
# glad_chromosomes = (da.from_zarr(os.path.join(zarr_path, "variant_contig")) + 1).compute()
# glad_positions = da.from_zarr(os.path.join(zarr_path, "variant_position")).compute()


# def match_query(embedding, query_embedding, metric="euclidean", weights=None):
#     kwargs = {}
#     if metric == "wminkowski":
#         kwargs["w"] = weights
#     distances = cdist(query_embedding, embedding, metric=metric, **kwargs)
#     return np.array(linear_sum_assignment(distances)[1])

@app.route("/")
def home():
    # os.environ.get('SECRET_KEY')
    return render_template("index.html")

@app.route("/visualize")
def visualize():
    df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/plotable.csv"), index_col=0)
    fig = px.scatter(df, x='UMAP2d 1', y='UMAP2d 2', color="Cohort", symbol=None, hover_name=df.index, hover_data=['Population', 'Country', 'State', 'City', 'Sex', 'Ethnicity'], render_mode='webgl')
    # fig = px.scatter_3d(df, x='UMAP3d 1', y='UMAP3d 2', z='UMAP3d 3', color="Dataset", symbol=None, hover_name=df.index, hover_data=['Population', 'Country', 'State', 'City', 'Sex', 'Ethnicity'], render_mode='webgl')
    fig.update_layout(height=800)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("visualize.html", graphJSON=graphJSON)

@app.route("/find-controls", methods=["GET", "POST"])
def find_controls():
    if request.method == "POST":
        if "file" not in request.files or len(request.files["file"].filename) == 0:
            flash("Select a valid numpy file")
            return redirect(request.url)
        else:
            resp = requests.post("http://localhost:9090/match", data=request.files["file"])
            return resp.content, 200
            # return resp
            # query_pca = np.load(request.files["file"])
            # match_indices = match_query(glad_pca, query_pca, metric="wminkowski", weights=explained_variance_ratio)
            # match_allele_frequencies = (glad_genotypes[:, match_indices].sum(-1).sum(-1) / (glad_genotypes.shape[1] * glad_genotypes.shape[2])).compute()
            # buffer = io.BytesIO()
            # np.savez_compressed(buffer, chromosomes=glad_chromosomes, positions=glad_positions, minor_allele_frequencies=match_allele_frequencies)
            # buffer.seek(0)
            # return send_file(buffer, attachment_filename="allele_frequencies.npz", as_attachment=True)
    return render_template("find_controls.html")

@app.route("/download-principal-components")
def download_principal_components():
    principal_components_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/data/Freeze1.imputed_above0.9.missing0.001.nodups_202106.sorted.biallelic.pruned_at0.5.filtered.principal_components.npy")
    return send_file(principal_components_path, attachment_filename="glad_principal_components.npy", as_attachment=True)
