# model-zoo-cookiecutter

This cookiecutter facilitates adding an example to the BIDS Stats Model zoo.

In order to use this cookiecutter, you must have a DataLad remote dataset available that contains the data you wish to use.

The cookiecutter will create a directory for your example, and install a DataLad submodule for the dataset (and optionally preprocessed dataset) you wish to use.
If not provided, the cookiecutter will create a template BIDS Stats Model file and a template MyST Markdown document for you, that you can edit to create your example.

## How to use this cookiecutter?
Reproduce the python environment using the requirements.txt. 

**1. Run make_exhibit to create the template:**
```
python make_exhibit.py
```

**2.Enter your model's information:** 
You will be asked for the following information:
```
"dataset_url": "URL of the dataset you wish to use",
"preproc_url": "URL of the preprocessed dataset you wish to use",
"exhibit_name": "Name of the exhibit folder name",
"author_name": "Your name (or your organization/team)",
"description": "A short description of the example.",
"model_json_path": "Path to BIDS StatsModel file ending in _smdl.json",
"scan_length": "Scan length (in seconds). This is used to calculate design matrices without fetching the data."
```

**3. This cookiecutter creates the following directory tree:**
```
{exhibit_name}
├── [dataset-name]
├── [preproc-dataset-name]
├── model-{example_name}_smdl.json
├── model-{example_name}_smdl.md
```

