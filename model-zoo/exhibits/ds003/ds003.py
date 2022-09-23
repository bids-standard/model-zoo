# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
# %load_ext autoreload
# %autoreload 2

import json
from pathlib import Path
from itertools import chain

import numpy as np
import pandas as pd

# %% [markdown]
# # Preamble
# We will use Datalad to manage our data, which in turn depends on git-annex. To install git-annex, uncomment and run one of the following:

# %%
# Debian
# apt-get install git-annex

# %%
# Linux with Conda
# conda install -y git-annex

# %%
# OSX
# open https://git-annex.branchable.com/install/OSX/

# %% [markdown]
# Datalad, Pybids, Nilearn are Python tools.
# To ensure that everything installs correctly, we'll upgrade the [pip](https://pip.pypa.io/en/stable/) package manager
# and the [setuptools](https://setuptools.readthedocs.io/en/latest/) utilities.
#
# We will also install unreleased versions of Datalad, Pybids, and [Nilearn](https://nilearn.github.io/) to make things run a little more smoothly.

# %%
# # ! pip install -q --upgrade pip setuptools
# # ! pip install -q --upgrade datalad nistats pybids graphviz


# %%
# # get the dataset
# # !export DATALAD_UI_PROGRESSBAR=log
# # !export NO_COLOR="1"

# # !datalad install -r ds000003-fmriprep/
# # !datalad update ds000003_fmriprep

# # !datalad install -r ds000003/
# # !datalad update ds000003

# %%
# # ! datalad get ds000003-fmriprep/sub-*/func/*_desc-confounds_*.tsv \
# #               ds000003-fmriprep/sub-*/func/*_desc-confounds_*.json \
# #               ds000003-fmriprep/dataset_description.json 

# %%
from nilearn.plotting import plot_design_matrix

import bids
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout


def api(obj):
    return {attr: getattr(obj, attr) for attr in dir(obj) if not attr[0] == '_'}


# %%
layout = BIDSLayout('./ds000003', derivatives='./ds000003-fmriprep')

# %%
json_file = 'model-001_smdl.json'
spec = json.loads(Path(json_file).read_text())
spec

# %%
layout

# %%
graph = BIDSStatsModelsGraph(layout, spec)

# %%
root_node = graph.root_node

# %%
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=320)

# %%
collections = layout.get_collections('run', task='rhymejudgment', scan_length=320)

# %%
root_node.get_collections()[-1].entities

# %%
# graph.load_collections(scan_length=320)

# %%
# foo = graph.root_node.get_collections()[0]

# %%
# [ff.run_info[0][0]['RepetitionTime'] for ff in list(foo.variables.values())]

# %%
# for ff in list(foo.variables.values()):
#     break

# %%
# ff.to_df()

# %%
specs = root_node.run(group_by=root_node.group_by)
len(specs)

# %%
specs[0]

# %%
plot_design_matrix(specs[0].X, rescale=False)
