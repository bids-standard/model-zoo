---
jupytext:
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

```{code-cell} ipython3
%load_ext autoreload
%autoreload 2

import json
from pathlib import Path
from itertools import chain

import numpy as np
import pandas as pd
```

# Preamble
We will use Datalad to manage our data, which in turn depends on git-annex.

```{code-cell} ipython3
! datalad get ds000003-fmriprep/sub-*/func/*_desc-confounds_*.tsv \
              ds000003-fmriprep/sub-*/func/*_desc-confounds_*.json \
              ds000003-fmriprep/dataset_description.json 
```

```{code-cell} ipython3
from nilearn.plotting import plot_design_matrix

import bids
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout


def api(obj):
    return {attr: getattr(obj, attr) for attr in dir(obj) if not attr[0] == '_'}
```

```{code-cell} ipython3
layout = BIDSLayout('./ds000003', derivatives='./ds000003-fmriprep')
```

```{code-cell} ipython3
json_file = 'model-001_smdl.json'
spec = json.loads(Path(json_file).read_text())
spec
```

```{code-cell} ipython3
layout
```

```{code-cell} ipython3
graph = BIDSStatsModelsGraph(layout, spec)
```

```{code-cell} ipython3
root_node = graph.root_node
```

```{code-cell} ipython3
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=320)
```

```{code-cell} ipython3
collections = layout.get_collections('run', task='rhymejudgment', scan_length=320)
```

```{code-cell} ipython3
root_node.get_collections()[-1].entities
```

```{code-cell} ipython3
graph.load_collections(scan_length=320)
```

```{code-cell} ipython3
specs = root_node.run(group_by=root_node.group_by)
len(specs)
```

```{code-cell} ipython3
specs[0]
```

```{code-cell} ipython3
plot_design_matrix(specs[0].X, rescale=False)
```
