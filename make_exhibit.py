import click
from os import chdir
from pathlib import Path
from cookiecutter.main import cookiecutter
from datalad.core.distributed.clone import decode_source_spec


@click.command()
@click.option('--exhibit-name',
        help="Name of the exhibit.",
        required=True,
        type=str
)
@click.option('--model-json-path',
       help="Path to BIDS StatsModel file ending in _smdl.json. If not provided, a default model will be placed in the exhibit folder.",
       default="model-default_smdl.json",
       type=str
)
@click.option('--dataset-url',
        help="DataLad URL of the RAW dataset to install. If not provided, no dataset will be installed, and user will have to manually install it.",
        default="None",
        type=str
)
@click.option('--preproc-url',
        help="DataLad URL of the PREPROCESSED dataset. If None, its assumed the preprocessed data is under /derivatives/ in the RAW dataset.",
        type=str,
        default="None"
)
@click.option('--scan-length',
        help="Length of the scan in seconds.",
        type=int,
)
@click.option('--description',
        help="Description of the exhibit.",
        type=str,
        default="Description of the exhibit."
)
@click.option(
    '--toc/--no-toc', 
    default=True,
    help='Update the table of contents with new example?'
)
def make_exhibit(exhibit_name, model_json_path, dataset_url, preproc_url, scan_length, description, toc):
    context = {
        'exhibit_name': exhibit_name,
        'dataset_url': dataset_url,
        'preproc_url': preproc_url,
        'scan_length': scan_length,
        'description': description,
        'toc': toc
    }

    # Determine absolute & relative path to model JSON file
    if model_json_path == "model-default_smdl.json":
        model_json_path = str(Path(context['exhibit_name']) / "model-default_smdl.json")
    else:
        model_json_path = str(Path(model_json_path).absolute())

    model_json_rel_path = Path(model_json_path).name

    context['model_json_path'] = model_json_path
    context['model_json_rel_path'] = model_json_rel_path # This path is the one that will be used in the markdown report

    # Preprocess datalaset URLs (decode to get the path)
    context['dataset_path'] = str(Path("data-raw") / decode_source_spec(context['dataset_url'])['default_destpath'])

    if context['preproc_url'] != "None":
        context['preproc_path'] = str(Path("data-preproc") / decode_source_spec(context['preproc_url'])['default_destpath'])
    else:
        context['preproc_path'] = True

    # Move into exhibit directory

    chdir('model-zoo/exhibits')

    # Run cookiecutter
    cookiecutter(
        '_template',
        no_input=True,
        extra_context=context
    )


if __name__ == "__main__":
    make_exhibit()
