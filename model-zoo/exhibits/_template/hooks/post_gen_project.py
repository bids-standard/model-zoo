from datalad.api import install
from os import chdir
from pathlib import Path
import shutil

exhibit_name = '{{ cookiecutter.exhibit_name }}'

dataset_url = '{{ cookiecutter.dataset_url }}'
preproc_url = '{{ cookiecutter.preproc_url }}'
model_json_path = '{{ cookiecutter.model_json_path }}'

report_path = Path(f'model-default_smdl.md')

# Install the RAW dataset
if dataset_url != "None":
    print("Installing RAW dataset...")
    dataset = install(source=dataset_url)

# Install the PREPROCESSED dataset
if preproc_url != "None":
    print("Installing preproc dataset...")
    preproc = install(source=preproc_url)


default_json = Path("model-default_smdl.json")
# If user provided a model, copy it to the exhibit folder, and delete the default model
if "model-default_smdl.json" not in model_json_path:
    # Copy the model to the exhibit folder
    target_json = Path(model_json_path)
    shutil.copy(target_json, '.')

    # Delete default model
    default_json.unlink()

    # Rename report
    report_path.rename(f'{target_json.stem}.md')

## TODO:
## Add datasets as git submodules

