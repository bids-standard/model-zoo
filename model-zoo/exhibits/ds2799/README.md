# Run a dummy GLM on resting state data

Applies a GLM on resting state data from ds002799
with an approach similar to that used in the cluster failure paper.

## Getting the data for 2 subjects

To run from `model-zoo/exhibits/ds2799/`:

model-zoo/exhibits/ds2799/ds002799/derivatives/fmriprep

```bash
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29*/ses-*/func/*tsv -J 12
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29*/ses-*/func/*json -J 12
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29*/ses-*/func/*task-rest*MNI* -J 12
```

## Creating dummy events

Run the script `add_dummy_events.py` to create dummy events.


## Running the analysis

```bash
sourcedata=$PWD
output_dir=$PWD/derivatives
tmp_dir=$PWD/tmp

model_file=model-ds2799_desc-clusterFailure_smdl.json

mkdir -p ${tmp_dir} ${output_dir}

docker run --rm -it \
    -v ${sourcedata}:/sourcedata \
    -v ${tmp_dir}:/scratch \
    -v ${output_dir}:/output \
        poldracklab/fitlins:0.11.0 \
            --verbose \
            --model /sourcedata/${model_file} \
            -d /sourcedata/ds002799/derivatives/fmriprep \
            --work-dir /scratch \
            --participant-label 292 294 \
            --space MNI152NLin2009cAsym \
            --desc-label preproc \
            --estimator nilearn \
            --drift-model cosine \
            --smoothing 6:run:iso \
            /sourcedata/ds002799 /output run
```