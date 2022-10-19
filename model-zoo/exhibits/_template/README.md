# make_exhibit.py

This cookiecutter wrapper facilitates adding an example to the BIDS Stats Model zoo.

The only requirement is to have a unique exhibit name. The script will create a directory with the exhibit name, and populate it with a template exhibit and a template dataset.

Ideally, you should also provide a remote Datalad URL for the dataset you are using (and separate processed dataset if necessary).

If so, the script will install the datasets under the exhibit and register them as git submodules to this project. 

You may also provide an exhibit BIDS Stats Model JSON file ending in `_smdl.json`, which will be copied into  your exhibit. 
If not provided, the script will create a template BIDS Stats Model file (`model-default_smdl.json`) and a template MyST Markdown document for you (`model-default_smdl.md`), that you can edit to create your example.

## How to use this cookiecutter?
Reproduce the python environment using the requirements.txt. 

**1. Run make_exhibit to create the template:**
```
python make_exhibit.py
```

**2.Enter your model's information:** 

You will be asked for the following information:

```
Usage: make_exhibit.py [OPTIONS]

Options:
  --exhibit-name TEXT     Name of the exhibit. This will be the name of the
                          folder that will be created under model-
                          zoo/exhibits.  [required]
  --model-json-path TEXT  Path to a BIDS Stats Model file ending in
                          _smdl.json. File will be copied into the exhibit
                          folder.          If not provided, an incomplete
                          default model will be placed in the exhibit folder
                          as a starting point.
  --dataset-url TEXT      DataLad URL of the RAW dataset to install as a
                          submodule. If not provided, no dataset will be
                          installed, and user will have to manually install it
                          later.
  --preproc-url TEXT      DataLad URL of the PREPROCESSED dataset. If None,
                          its assumed the preprocessed data is under
                          /derivatives/ in the RAW dataset.
  --scan-length INTEGER   Length of the scan in seconds. Used to create design
                          matices without downloading functional images.
  --description TEXT      Description of the BIDS Stats Model.
  --toc / --no-toc        Update the table of contents with new example?
  --help                  Show this message and exit.
```

**3. This cookiecutter creates the following directory tree:**
```
{exhibit_name}
├── [dataset-name]
├── [preproc-dataset-name]
├── model-{example_name}_smdl.json
├── model-{example_name}_smdl.md
```

