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
# ! pip install -q --upgrade pip setuptools
# ! pip install -q --upgrade datalad nistats pybids graphviz


# %%
# get the dataset
# !export DATALAD_UI_PROGRESSBAR=log
# !export NO_COLOR="1"

# !datalad install -r ds000003-fmriprep/
# !datalad update ds000003_fmriprep

# !datalad install -r ds000003/
# !datalad update ds000003

# %%
# ! datalad get ds000003-fmriprep/sub-*/func/*_desc-confounds_*.tsv \
#               ds000003-fmriprep/sub-*/func/*_desc-confounds_*.json \
#               ds000003-fmriprep/dataset_description.json 

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
graph.write_graph(format='svg')

# %%
root_node = graph.root_node

# %%
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=320)

# %%
graph.load_collections(scan_length=320)

# %%
foo = graph.root_node.get_collections()[0]

# %%
[ff.run_info[0][0]['RepetitionTime'] for ff in list(foo.variables.values())]

# %%
for ff in list(foo.variables.values()):
    break

# %%
ff.to_df()

# %%
specs = root_node.run(group_by=root_node.group_by)
len(specs)

# %%
api(specs[0])

# %%
specs[0]

# %%
specs[0].X

# %%
plot_design_matrix(specs[0].X, rescale=False)

# %%
specs[0].entities

# %%
specs[0].metadata

# %%
bold = layout.get(**specs[0].entities, suffix='bold', extension='.nii.gz')[0]

# %%
# import nilearn.glm
# l1m = nilearn.glm.first_level.FirstLevelModel()
# l1m.fit(bold.get_image(), design_matrices=specs[0].X)

# %%
next_node = root_node.children[0].destination

# %%
next_node.group_by

# %%
root_node.children[0].filter

# %%
contrasts = list(chain(*[s.contrasts for s in specs]))
sub_specs = next_node.run(contrasts, group_by=next_node.group_by)

# %%
api(sub_specs[3])

# %%
# %pdb

# %%
ds1_node = next_node.children[1].destination
api(ds1_node)

# %%
next_node.children[1].filter

# %%
sub_contrasts = list(chain(*[s.contrasts for s in sub_specs]))
ds1_specs = ds1_node.run(sub_contrasts, group_by=ds1_node.group_by, **next_node.children[1].filter)

# %%
ds1_specs[0].X

# %%
pd.concat((ds1_specs[0].data, ds1_specs[0].metadata), axis=1)

# %%
ds1_specs[0].contrasts

# %%
ds0_node = next_node.children[0].destination
ds0_specs = ds0_node.run(sub_contrasts, group_by=ds0_node.group_by)

# %%
ds0_specs

# %%
ds0_specs[1].X

# %%
pd.concat((ds0_specs[0].data, ds0_specs[0].metadata), axis=1)

# %%
ds2_node = next_node.children[2].destination
filters = next_node.children[2].filter or {}
print(filters)
ds2_specs = ds2_node.run(sub_contrasts, group_by=ds2_node.group_by, **filters)
print(ds2_specs)

# %%
api(ds2_specs[0])

# %%
ds2_specs[0].X

# %%
pd.concat((ds2_specs[0].data, ds2_specs[0].metadata), axis=1)

# %%
api(ds1_node)

# %%
graph.nodes

# %%
graph.root_node.children

# %%
graph.root_node.children[0].destination.children

# %%
graph.root_node.children[0].destination.children[2].destination.name

# %%
© 2022
GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact
GitHub
Pricing
API
Training
Blog
About
Loading
complete
