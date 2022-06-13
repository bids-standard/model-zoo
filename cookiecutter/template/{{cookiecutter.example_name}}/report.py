# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import json
import pandas as pd
import numpy as np
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout
from pathlib import Path
from nilearn.plotting import plot_design_matrix

# %% [markdown]
# # {{cookiecutter.example_name}}

# %% [markdown]
# #### Set Up
# Instantiate the `BIDSLayout` to index the dataset, and load `BIDS Stats Model` JSON document

# %%
# Variables provided using cookiecutter
dataset_path = Path(f'{{cookiecutter.dataset_path}}')
example_name = f'{{cookiecutter.example_name}}'
scan_length = {{cookiecutter.scan_length}}
derivatives = '{{cookiecutter.derivatives}}'

# %%
if derivatives == 'None':
    layout = BIDSLayout(f'{dataset_path}')
else:
    layout = BIDSLayout(f'{dataset_path}', derivatives=derivatives)

# %% [markdown]
# #### Model & model graph

# %%
model_json = f'model/model-{example_name}_smdl.json'
print(f'Model Name: {model_json}')
with open(model_json, 'r') as j:
     spec = json.loads(j.read())
spec

# %%
graph = BIDSStatsModelsGraph(layout, spec)

# %%
graph.write_graph(format='svg')

# %% [markdown]
# First, let's load collections of variables from the Dataset for the entire Graph

# %%
try:
    graph.load_collections()
except ValueError:
    scan_length=scan_length # Set scan length to avoid downloadin images
    graph.load_collections(scan_length=scan_length)

# %% [markdown]
# #### Run-level node
#
# Let's look at the run-level node

# %%
specs = graph.root_node.run()
len(specs)

# %%
# Design matrix for first run
specs[0].X

# %%
plot_design_matrix(specs[0].X)

# %%
specs[0].entities

# %%
specs[0].metadata

# %%
next_node = graph.root_node.children[0].destination

# %%
next_node.group_by
