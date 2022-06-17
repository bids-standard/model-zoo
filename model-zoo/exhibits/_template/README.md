# model-zoo-cookiecutter

## How to use this cookiecutter?
Reproduce the python environment using the requirements.txt. 

**1. Run cookiecutter to create the template:**
```
cookiecutter template
```

**2.Enter your model's information:** 
You will be asked for the following information:
```
"example_name": "example_name",
"author_name": "Your name (or your organization/team)",
"description": "A short description of the example.",
"dataset_path": "The local path to the dataset being used"
"model_json_path": "Path to the json describing the model",
"scan_length": "Scan length. Can be inferred from the images if these are
availiable",
"derivatives": "Path to the fmriprep derivatives. If no derivatives are
availiable type None."
```
Note: To use this cookiecutter you will need to have already downloaded the data
that you want to analyze and have already defined a `model.json` that describes
the BIDS Stats Models. 


**3. This cookiecutter creates the following directory tree:**
```
{example_name}
├── README.md
├── data
    └── data -> symbolic link to the data 
├── model
│   └── model-{example_name}_smdl.json -> symbolic link to the passed model file
└── report.py
```

