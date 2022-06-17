import subprocess
from pathlib import Path
import os
import subprocess

# Create a symlink to the dataset using the provided path
dataset_path = Path(f'{{cookiecutter.dataset_path}}')
example_name = f'{{cookiecutter.example_name}}'
json_path = Path('{{cookiecutter.model_json_path}}')

if dataset_path.exists():
    subprocess.call(f'ln -s {dataset_path} data/', shell=True)

# Create a symlink to provided model.json
if json_path.exists():
    os.symlink(json_path, f'model/model-{example_name}_smdl.json')
