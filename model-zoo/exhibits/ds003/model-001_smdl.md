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

```{code-cell}
%load_ext autoreload
%autoreload 2

import json
from pathlib import Path
from itertools import chain

import numpy as np
import pandas as pd
```

# Preamble
We will use Datalad to manage our data, which in turn depends on git-annex. To install git-annex, uncomment and run one of the following:

```{code-cell}
# Debian
# apt-get install git-annex
```

```{code-cell}
# Linux with Conda
# conda install -y git-annex
```

```{code-cell}
# OSX
# open https://git-annex.branchable.com/install/OSX/
```

Datalad, Pybids, Nilearn are Python tools.
To ensure that everything installs correctly, we'll upgrade the [pip](https://pip.pypa.io/en/stable/) package manager
and the [setuptools](https://setuptools.readthedocs.io/en/latest/) utilities.

We will also install unreleased versions of Datalad, Pybids, and [Nilearn](https://nilearn.github.io/) to make things run a little more smoothly.

```{code-cell}
# ! pip install -q --upgrade pip setuptools
# ! pip install -q --upgrade datalad nistats pybids graphviz
```

```{code-cell}
# # get the dataset
# !export DATALAD_UI_PROGRESSBAR=log
# !export NO_COLOR="1"

# !datalad install -r ds000003-fmriprep/
# !datalad update ds000003_fmriprep

# !datalad install -r ds000003/
# !datalad update ds000003
```

```{code-cell}
# ! datalad get ds000003-fmriprep/sub-*/func/*_desc-confounds_*.tsv \
#               ds000003-fmriprep/sub-*/func/*_desc-confounds_*.json \
#               ds000003-fmriprep/dataset_description.json 
```

```{code-cell}
from nilearn.plotting import plot_design_matrix

import bids
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout


def api(obj):
    return {attr: getattr(obj, attr) for attr in dir(obj) if not attr[0] == '_'}
```

```{code-cell}
layout = BIDSLayout('./ds000003', derivatives='./ds000003-fmriprep')
```

```{code-cell}
json_file = 'model-001_smdl.json'
spec = json.loads(Path(json_file).read_text())
spec
```

```{code-cell}
layout
```

```{code-cell}
graph = BIDSStatsModelsGraph(layout, spec)
```

```{code-cell}
root_node = graph.root_node
```

```{code-cell}
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=320)
```

```{code-cell}
collections = layout.get_collections('run', task='rhymejudgment', scan_length=320)
```

```{code-cell}
root_node.get_collections()[-1].entities
```

```{code-cell}
# graph.load_collections(scan_length=320)
```

```{code-cell}
# foo = graph.root_node.get_collections()[0]
```

```{code-cell}
# [ff.run_info[0][0]['RepetitionTime'] for ff in list(foo.variables.values())]
```

```{code-cell}
# for ff in list(foo.variables.values()):
#     break
```

```{code-cell}
# ff.to_df()
```

```{code-cell}
specs = root_node.run(group_by=root_node.group_by)
len(specs)
```

```{code-cell}
specs[0]
```

```{code-cell}
plot_design_matrix(specs[0].X, rescale=False)
```
