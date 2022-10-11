---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3.9.7 ('base')
  language: python
  name: python3
---

# Neuroimaging Analysis Replication and Prediction Study (NARPS)

+++

Here, we specify the statistical model in the [NARPS](https://www.narps.info/) study using a _BIDS Stats Model_. 

The dataset is publicaly available on [OpenNeuro](https://openneuro.org/datasets/ds001734/).

+++

#### Setup

```{code-cell} ipython3
import json
from pathlib import Path
from itertools import chain

import numpy as np
import pandas as pd

from nilearn.plotting import plot_design_matrix

import bids
from bids.modeling import BIDSStatsModelsGraph
from bids.layout import BIDSLayout
```

First, we set up the `BIDSLayout` object...

```{code-cell} ipython3
layout = BIDSLayout('./ds001734/')
```

... and load the _BIDS Stats Model_ JSON specification:

```{code-cell} ipython3
json_file = './model-narps_smdl.json'
spec = json.loads(Path(json_file).read_text())
spec
```

### Initializing Model

+++

Here, we modify the model to restrict it to a single task and three subjects (for demonstration purposes), and initialize the `BIDSStatsModelGraph` object:

```{code-cell} ipython3
spec['Input'] = {
    'task': 'MGT',
    'subject': ['001', '002', '003']
}

graph = BIDSStatsModelsGraph(layout, spec)
```

We can visualize the model as a graph:

```{code-cell} ipython3
graph.write_graph(format='svg')
```

This graph specifices that a _run_ level model should be run on every subject / run combination, followed by a _subject_ level model, which combines the results of the _run_ level models.

Finally, at the group level, we have three distinct models: a between-group comparison of the 'loss' contrast, and within-group one-sample t-tests for the 'loss' and 'positive' contrasts.

We'll take a closer look later.

+++

### Populating the Graph

In order to compute the precise design matrices for each level of the model, we need to populate the graph with the specific variables, and outputs from each `Node` to the next.

First, we load the `BIDSVariableCollection` objects, for the entire graph:

```{code-cell} ipython3
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=453)  # TR = 1, nvols = 453; necessary if no BOLD data
```

We can look at the variables available to the root node of the Graph:

```{code-cell} ipython3
root_node = graph.root_node
colls = root_node.get_collections()
colls
```

```{code-cell} ipython3
root_node.group_by
```

Note that there are multiple instances of the root node, one for each subject / run combination (the node's `group_by` is : `['run', 'subject']`). We can access the variables for a specific instance of the root node using `variables`:

```{code-cell} ipython3
colls[0].variables
```

## Running nodes
Although the graph has defined how `Nodes` and `Edges` are related, it has not yet defined the specific design matrices for each, as this requires knowing the specific variables associated with each `Node`. We can now run the graph to populate the design matrices for each `Node`:

```{code-cell} ipython3
specs = root_node.run(group_by=root_node.group_by, force_dense=False)
```

For each instance of the root node, a `BIDSStatsModelsNodeOutput` object is created, which contains the model specification, and final design matrix for each:

```{code-cell} ipython3
specs
```

```{code-cell} ipython3
first_run = specs[0]
```

For each, we can access key aspects of the model specification:

```{code-cell} ipython3
first_run.entities
```

```{code-cell} ipython3
# Final design matrix
first_run.X
```

```{code-cell} ipython3
# Plot design matrix
plot_design_matrix(specs[0].X)
```

Finally, these are the contrasts for the root node:

The contrasts specify the outputs of the `Node` that will be passed to subsequent Nodes

```{code-cell} ipython3
# Contrast specification
first_run.contrasts
```

### Subject-level model

+++

Now that we have populated the design matrices for the run-level root node `Node`, we can advance the graph to the next level, and repeat the process.

Here, the subsequent `Node` is a `subject` level fixed-effects meta-analysis model, which comibines run estimates, separately for each combination of `contrast` and `subject`.

```{code-cell} ipython3
next_node = root_node.children[0].destination
```

```{code-cell} ipython3
next_node.level
```

```{code-cell} ipython3
next_node.group_by
```

In order to populate the `subject` level node, we need to pass the outputs from the previous `run` level `Node` as inputs to the subsequent `Node`.

```{code-cell} ipython3
contrasts = list(chain(*[s.contrasts for s in specs]))
```

Since the `subject` level `Node` is `group_by` : `['subject', 'contrast']`, each combination of `subject` and `contrast` will have a separate `BIDSStatsModelsNodeOutput` object:

```{code-cell} ipython3
sub_specs = next_node.run(contrasts)
sub_specs
```

Taking a look at a single Nodes's specification, the design matrix (`X`) is:

```{code-cell} ipython3
sub_specs[3].X
```

In this case, we are applying a simple intercept model which is equivalent to a one-sample t-test.

To understand which inputs are associated with this design, we can look at the `metadata` attribute:

```{code-cell} ipython3
sub_specs[3].metadata
```

Finally the contrast for this `Node` simply passes forward the intercept:

```{code-cell} ipython3
sub_specs[3].contrasts
```

### Group-level Nodes

Remember that the group-level of this model, we defined three separate `Nodes`, each performing a different analysis.

- "positive" is a within-group one-sample t-test of all contrasts.

- "negative-loss" is a within-group one-sample t-test for the 'loss' contrast, but reversed such that the positive direction is negative.

- "between-groups" is a between-group comparison of the 'loss' contrast.

Let's take a look at each separately:

+++

#### "Positive" Node (Within-Groups)

+++

Let's look at the original definition of this `Node` and the corresponding `Edge` in the original JSON specification:

```{code-cell} ipython3
spec['Nodes'][3]
```

```{code-cell} ipython3
spec['Edges'][1]
```

This `Node` specifies to run a separate one-sample t-test for each contrast, for each group separately (`'GroupBy': ['contrast', 'group']`)

```{code-cell} ipython3
# Prepare subject-level Node output contrasts
sub_contrasts = list(chain(*[s.contrasts for s in sub_specs]))

# Run "positive" Node
ds0_node = next_node.children[0].destination 
ds0_specs = ds0_node.run(sub_contrasts)
```

There are unique `BIDSStatsModelsNodeOutput` objects (and thus, models) for each contrast / group combiation:

```{code-cell} ipython3
ds0_specs
```

Taking a look at this first, we can see the model is a simple intercept model, which is equivalent to a one-sample t-test:

```{code-cell} ipython3
ds0_specs[0].X
```

With the following inputs:

```{code-cell} ipython3
ds0_specs[0].metadata
```

#### "Negative-Loss" Node (Within-Groups)

+++

Next, the "negative-loss" Node takes _only_ the 'loss' contrast, and reverses the sign of the positive direction, such that the positive direction is negative.

In the `Contrast` section of the model, we specify the weight as -1 to flip the sign.

```{code-cell} ipython3
# Negative-loss node specification
spec['Nodes'][4]
```

The corresponding `Edge` specifies to `Filter` the input to only include the 'loss' contrast:

```{code-cell} ipython3
spec['Edges'][3]
```

```{code-cell} ipython3
ds1_node = next_node.children[1].destination
ds1_specs = ds1_node.run(sub_contrasts,**next_node.children[1].filter)
```

The design matrix for the group-level node peforms a simple one-sample t-test on the subject-level contrasts:

```{code-cell} ipython3
ds1_specs[0].X
```

```{code-cell} ipython3
ds1_specs[0].metadata
```

Finally, looking at the contrasts, we can see that the 'loss' contrast is passed forward, but with the positive direction flipped:

```{code-cell} ipython3
ds1_specs[0].contrasts
```

### Between-Groups Node specification

+++

Finally, the "between-groups" Node is a between-group comparison of the 'loss' contrast. 

Importantly, the `GroupBy` is set to `['contrast']`, such that the model is run separately for each contrast, but the contrasts are combined across groups.

```{code-cell} ipython3
spec['Nodes'][-1]
```

In addition, this `Node` uses `Formula` notation to specify the model. The `C(group)` term specifies a categorical variable, which will be used to specify the between-group comparison.

In the `Contrast` section, we can refer to specific levels of the categorical variable using the `C()` notation. Here, we specify a contrast of `C(group)[T.equalRange] - C(group)[T.equalIndifference]`, with weights `[1, -1]`.

+++

As in the previous `Node`, the corresponding `Edge` specifies to `Filter` the input to only include the 'loss' contrast:

```{code-cell} ipython3
spec['Edges'][3]
```

```{code-cell} ipython3
# Running between-subject Node
ds2_node = next_node.children[2].destination 
filters = next_node.children[2].filter or {}
print(filters)
ds2_specs = ds2_node.run(sub_contrasts, **filters)
print(ds2_specs)
```

The design matrix (`X`) for this `Node` contrasts subjects 1 and 3 vs 2, as these subjects differ by `group`:

```{code-cell} ipython3
ds2_specs[0].X
```

```{code-cell} ipython3
ds2_specs[0].metadata
```
