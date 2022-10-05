---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# NARPS

```{code-cell} ipython3
%load_ext autoreload
%autoreload 2

import json
from pathlib import Path
from itertools import chain

import numpy as np
import pandas as pd

from nilearn.plotting import plot_design_matrix

import bids
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout

def api(obj):
    return {attr: getattr(obj, attr) for attr in dir(obj) if not attr[0] == '_'}
```

```{code-cell} ipython3
layout = BIDSLayout('./ds001734/', database_path="./ds001734.db")
```

```{code-cell} ipython3
json_file = './model-narps_smdl.json'
spec = json.loads(Path(json_file).read_text())
spec
```

```{code-cell} ipython3
spec['Input'] = {
    'task': 'MGT',
    'subject': ['001', '002', '003']
}
```

```{code-cell} ipython3
graph = BIDSStatsModelsGraph(layout, spec)
```

```{code-cell} ipython3
graph.write_graph(format='svg')
```

```{code-cell} ipython3
root_node = graph.root_node
```

```{code-cell} ipython3
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=453)  # TR = 1, nvols = 453
```

```{code-cell} ipython3
specs = root_node.run(group_by=root_node.group_by, force_dense=False)
```

```{code-cell} ipython3
api(specs[0])
```

```{code-cell} ipython3
specs[0]
```

```{code-cell} ipython3
plot_design_matrix(specs[0].X)
```

```{code-cell} ipython3
specs[0].entities
```

```{code-cell} ipython3
specs[0].metadata
```

```{code-cell} ipython3
bold = layout.get(**specs[0].entities, suffix='bold', extension='.nii.gz')[0]
```

```{code-cell} ipython3
# import nilearn.glm
# l1m = nilearn.glm.first_level.FirstLevelModel()
# l1m.fit(bold.get_image(), design_matrices=specs[0].X)
```

```{code-cell} ipython3
next_node = root_node.children[0].destination
```

```{code-cell} ipython3
next_node.group_by
```

```{code-cell} ipython3
root_node.children[0].filter
```

```{code-cell} ipython3
contrasts = list(chain(*[s.contrasts for s in specs]))
sub_specs = next_node.run(contrasts, group_by=next_node.group_by)
```

```{code-cell} ipython3
api(sub_specs[3])
```

```{code-cell} ipython3
ds1_node = next_node.children[1].destination
api(ds1_node)
```

```{code-cell} ipython3
next_node.children[1].filter
```

```{code-cell} ipython3
sub_contrasts = list(chain(*[s.contrasts for s in sub_specs]))
ds1_specs = ds1_node.run(sub_contrasts, group_by=ds1_node.group_by, **next_node.children[1].filter)
```

```{code-cell} ipython3
%debug
```

```{code-cell} ipython3
ds1_specs[0].X
```

```{code-cell} ipython3
pd.concat((ds1_specs[0].data, ds1_specs[0].metadata), axis=1)
```

```{code-cell} ipython3
ds1_specs[0].contrasts
```

```{code-cell} ipython3
ds0_node = next_node.children[0].destination 
ds0_specs = ds0_node.run(sub_contrasts, group_by=ds0_node.group_by)
```

```{code-cell} ipython3
ds0_specs
```

```{code-cell} ipython3
ds0_specs[1].X
```

```{code-cell} ipython3
pd.concat((ds0_specs[0].data, ds0_specs[0].metadata), axis=1)
```

```{code-cell} ipython3
ds2_node = next_node.children[2].destination 
filters = next_node.children[2].filter or {}
print(filters)
ds2_specs = ds2_node.run(sub_contrasts, group_by=ds2_node.group_by, **filters)
print(ds2_specs)
```

```{code-cell} ipython3
api(ds2_specs[0])
```

```{code-cell} ipython3
ds2_specs[0].X
```

```{code-cell} ipython3
pd.concat((ds2_specs[0].data, ds2_specs[0].metadata), axis=1)
```

```{code-cell} ipython3
api(ds1_node)
```

```{code-cell} ipython3
graph.nodes
```

```{code-cell} ipython3
graph.root_node.children
```

```{code-cell} ipython3
graph.root_node.children[0].destination.children
```

```{code-cell} ipython3
graph.root_node.children[0].destination.children[2].destination.name
```

```{code-cell} ipython3

```
