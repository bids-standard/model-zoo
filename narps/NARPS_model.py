# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

from itertools import chain
from pathlib import Path
import pandas as pd
import numpy as np
import bids
bids.config.set_option('extension_initial_dot', True)
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout
from bids.tests import get_test_data_path
from os.path import join
import json

def api(obj):
    return {attr: getattr(obj, attr) for attr in dir(obj) if not attr[0] == '_'}


# %%
layout = BIDSLayout('./ds001734/')

# %%
json_file = './model/model-narps_smdl.json'
spec = json.loads(Path(json_file).read_text())
spec

# %%
graph = BIDSStatsModelsGraph(layout, spec)

# %%
root_node = graph.root_node

# %%
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=453)  # TR = 1, nvols = 453

# %%
specs = root_node.run(group_by=root_node.group_by, force_dense=False)
len(specs)

# %%
api(specs[0])

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
contrasts = list(chain(*[s.contrasts for s in specs]))
sub_specs = next_node.run(contrasts, group_by=next_node.group_by)

# %%
api(sub_specs[3])

# %%
ds1_node = next_node.children[1].destination
api(ds1_node)

# %%
sub_contrasts = list(chain(*[s.contrasts for s in sub_specs]))
ds1_specs = ds1_node.run(sub_contrasts, group_by=ds1_node.group_by)

# %%
ds1_specs[0].X

# %%
pd.concat((ds1_specs[0].data, ds1_specs[0].metadata), axis=1)

# %%
ds0_node = next_node.children[0].destination 
ds0_specs = ds0_node.run(sub_contrasts, group_by=ds0_node.group_by)

# %%
ds0_specs[0].X

# %%
pd.concat((ds0_specs[0].data, ds0_specs[0].metadata), axis=1)

# %%
