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
import json
import pandas as pd
import numpy as np
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout
from pathlib import Path
from nilearn.plotting import plot_design_matrix
```

#### Set Up
Instantiate the `BIDSLayout` to index the dataset, and load `BIDS Stats Model` JSON document

```{code-cell}
# Variables provided using cookiecutter
dataset_path = "{{ cookiecutter.dataset_path }}"
preproc_path = {{ cookiecutter.preproc_path }}
exhibit_name = "{{ cookiecutter.exhibit_name }}"
scan_length = {{ cookiecutter.scan_length }}
model_json = "{{ cookiecutter.model_json_rel_path }}"
```

```{code-cell}
layout = BIDSLayout(dataset_path, derivatives=preproc_path)
```

#### Model & model graph

```{code-cell}
print(f'Model Name: {model_json}')
with open(model_json, 'r') as j:
     spec = json.loads(j.read())
spec
```

```{code-cell}
graph = BIDSStatsModelsGraph(layout, spec)
```

```{code-cell}
graph.write_graph(format='svg')
```

First, let's load collections of variables from the Dataset for the entire Graph

```{code-cell}
try:
    graph.load_collections()
except ValueError:
    scan_length=scan_length # Set scan length to avoid downloadin images
    graph.load_collections(scan_length=scan_length)
```

#### Run-level node

Let's look at the run-level node

```{code-cell}
specs = graph.root_node.run()
len(specs)
```

```{code-cell}
# Design matrix for first run
specs[0].X
```

```{code-cell}
plot_design_matrix(specs[0].X)
```

```{code-cell}
specs[0].entities
```

```{code-cell}
specs[0].metadata
```

```{code-cell}
next_node = graph.root_node.children[0].destination
```

```{code-cell}
next_node.group_by
```
