# BIDS stats model for SPM data sets

These models are meant to correspond to the stats model and analysis shown in
the SPM manual.

Datasets and corresponding sections of the SPM manuals are available from here:
https://www.fil.ion.ucl.ac.uk/spm/data/

To run those models with fitlins:

- create a virtual environment and install fitlins

```bash
virtualenv -p /usr/bin/python3.8 env
source env/bin/activate
pip install -r requirements.txt
```

- or get the filins docker image

```bash
docker pull poldracklab/fitlins:0.10.1
```

## Mother of all experiments (MoAE)

Simple block design: one subject, one run, one condition.

Original BIDS dataset available from:

https://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.bids.zip

Datasets are available on GIN as datalad datasets and also added as submodules
to this repository for convenience.

- raw: https://gin.g-node.org/SPM_datasets/spm_moae_raw
- frmriprep derivatives: https://gin.g-node.org/SPM_datasets/spm_moae_fmriprep

## Run with fitlins

Statistical model: `model-MoAE-desc-pybids_smdl.json`

Get the data with datalad

```bash
datalad get moae_raw
datalad get moae_fmriprep
```

Run either :

- `moae_run_fitlins.sh`
- `moae_run_fitlins_docker.sh`


## Face repetition priming

Event related design: : one subject, one run, 2 X 2 design.

Simple model: `spm-FaceRep_smdl.json`

Parametric model: `spm-FaceRepParametric_smdl.json`

Data on GIN:

- raw: https://gin.g-node.org/SPM_datasets/spm_facerep_raw
- fmriprep: https://gin.g-node.org/SPM_datasets/spm_facerep_fmriprep
- fitlins: https://gin.g-node.org/SPM_datasets/spm_facerep_fitlins
