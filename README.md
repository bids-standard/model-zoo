# model-zoo
Zoo of BIDS Stats Models

This is a collection of of "exhibits" demonstrating the capabilities of BIDS Stats Models across various datasets.


## Building the site

To build the Jupyter Book site, run the following command:

```bash
jupyter-book build model-zoo
```


## Adding a new exhibit
To add a new exhibit, create a new directory in the `exhibits` directory. The name of the directory can be the name of the dataset you are using, but is not strictly controlled. Within that directory, create at least one BIDS Stats Model (e.g, `model-<model_name>_smdl.json`). You should also provide a paired Markdown file called `model-<model_name>_smdl.md`. Finally, add this markdown file to the `_toc.yml` file in the root of the repository. 

### Automate using cookicutter

To make this process simpler, you can use cookie cutter to create the template for you. To do this, run the following command:

```bash
cookiecutter template
```

See [this guide](exhibits/_template/README.md) for more information.

### Dataset submodules
Within each exhibit, there should be at least one DataLad git submodule for each dataset used in the exhibit. For example, the `narps` exhibit has a submodule for the `ds001734` dataset. 

To load existing dataset submodules run: 
```bash
git submodule update --init --recursive
```

You can add a new datasets like so:

```bash
datalad install -d . -s <remote> <subds-path>
``` 

where `<remote>` is the URL of the dataset and `<subds-path>` is the path to the dataset within the exhibit directory.


### Pair notebooks to markdown documents
Exhibits are MyST Markdown documents (`.md`) with the same base name as a matching BIDS Stats Model file with a `.json` extenson. 
To facilitate editing and viewing of exhibits, we use a Jupyter Book environment. This allows you to edit MyST Markdown document as a Jupyter Notebook and see the results of the code cells in real time.

To enable this functionality, install jupyterlab and jupytext, and possibly manually enable the extension:

```bash
pip install jupyter-lab jupytext
jupyter serverextension enable jupytext
```

Then, run `jupyter lab` from the root of the repository.

This will open a Jupyter Lab environment in your browser. Navigate to the `model-zoo/exhibits` directory and open the exhibit document (`.md`) as a notebook by right clicking the file and selecting "Open with > Jupytext Notebook".

You will now be able to edit this document as a Jupyter Notebook. When you save the notebook, the paired MyST Markdown document will be updated, as well as a paired `.ipynb` file with the cell outputs. 

See the [Jupytext Documentation](https://jupytext.readthedocs.io/en/latest/paired-notebooks.html) for more information.
