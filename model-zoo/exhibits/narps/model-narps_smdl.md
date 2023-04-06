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

# Neuroimaging Analysis Replication and Prediction Study (NARPS)

+++

Here, we specify the statistical model in the [NARPS](https://www.narps.info/) study using a _BIDS Stats Model_. 

The dataset is publicaly available on [OpenNeuro](https://openneuro.org/datasets/ds001734/).

+++

#### Setup

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

### Initializing `BIDSStatsModelsGraph`

+++

Here, we modify the model to restrict it to a single task and three subjects (for demonstration purposes), and initialize the `BIDSStatsModelGraph` object:

```{code-cell} ipython3
spec['Input'] = {
    'task': 'MGT',
    'subject': ['001']
}

graph = BIDSStatsModelsGraph(layout, spec)
```

We can visualize the model as a graph:

```{code-cell} ipython3
graph.write_graph()
```

This graph specifices that a _run_ level model should be run on every subject / run combination, followed by a _subject_ level model, which combines the results of the _run_ level models.

Finally, at the group level, we have three distinct models: a between-group comparison of the 'loss' contrast, and within-group one-sample t-tests for the 'loss' and 'positive' contrasts.

+++

### Loading variables

In order to compute the precise design matrices for each level of the model, we need to populate the graph with the specific variables availablet to each `Node`

Here, we load the `BIDSVariableCollection` objects, for the entire graph:

```{code-cell} ipython3
try:
    graph.load_collections()
except ValueError:
    graph.load_collections(scan_length=227) # Necessary to define if no BOLD data
```

Let's take a look at the variable available at the root `run` level

```{code-cell} ipython3
root_node = graph.root_node
colls = root_node.get_collections()
colls
```

```{code-cell} ipython3
root_node.group_by
```

Note that there are multiple instances of the root node, one for each subject / run combination (the node's `group_by` is : `['run', 'subject']`).

We can access the variables for a specific instance of the root node using `variables`:

```{code-cell} ipython3
colls[0].variables
```

```{code-cell} ipython3
ents = colls[0].entities
print(f"Subject ID: {ents['subject']}, Run ID: {ents['run']}")
```

## Executing the graph
Although the graph has defined how `Nodes` and `Edges` are linked, and we've loaded variables, we need to execute the graph in order to obtain the precise design matrices of each `Node`.

Executing the graph will begin with the root (in this case `run`), apply transformations, create a design matrix, and define the node's outputs as determined by `Contrasts`.
The outputs are then passed via `Edges` on the subsquent `Node`, and the process is repetead, until the entire graph is populated


```{code-cell} ipython3
graph.run_graph()
```

For each instance of the root node, a `BIDSStatsModelsNodeOutput` object is created, which contains the model specification, and final design matrix for each:

+++

root_node = graph.root_node
len(root_node.outputs_)

+++

## Run-level Node
Let's take a look at the first output of the root node (i.e. `run` level)

```{code-cell} ipython3
first_run = root_node.outputs_[0]
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
plot_design_matrix(first_run.X)
```

The contrasts specify the outputs of the `Node` that will be passed to subsequent Nodes

```{code-cell} ipython3
# Contrast specification
first_run.contrasts
```

## Subject-level Node

+++

The `subject` node in this case is a fixed-effects meta-analysis model, which comibines run estimates, separately for each combination of `contrast` and `subject`.

We can see how the root node connects to `subject`, via an `Edge`:

```{code-cell} ipython3
edge = root_node.children[0]
```

```{code-cell} ipython3
edge
```

```{code-cell} ipython3
subject_node = edge.destination
subject_node
```

```{code-cell} ipython3
subject_node.level
```

```{code-cell} ipython3
subject_node.group_by
```

Since the `subject` level `Node` is `group_by` : `['subject', 'contrast']`, each combination of `subject` and `contrast` will have a separate `BIDSStatsModelsNodeOutput` object:

```{code-cell} ipython3
sub_specs = subject_node.outputs_
sub_specs
```

Taking a look at a single Nodes's specification, the design matrix (`X`) is:

```{code-cell} ipython3
sub_specs[0].X
```

In this case, we are applying a simple intercept model which is equivalent to a one-sample t-test.

To understand which inputs are associated with this design, we can look at the `metadata` attribute:

```{code-cell} ipython3
sub_specs[0].metadata
```

Finally the contrast for this `Node` simply passes forward the intercept estimate:

```{code-cell} ipython3
sub_specs[0].contrasts
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
# Run "positive" Node
ds0_node = subject_node.children[0].destination 
ds0_specs = ds0_node.outputs_
```

```{code-cell} ipython3
ds0_node
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
ds1_node = subject_node.children[1].destination
ds1_specs = subject_node.outputs_
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
# Get next node from subject
ds2_node = subject_node.children[2].destination 
ds2_specs = ds2_node.outputs_
```

The design matrix (`X`) for this `Node` contrasts subjects 1 and 3 vs 2, as these subjects differ by `group`:

```{code-cell} ipython3
ds2_specs[0].X
```

```{code-cell} ipython3
ds2_specs[0].metadata
```
