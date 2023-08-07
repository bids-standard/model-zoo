# Run a dummy GLM on resting state data

Applies a GLM on resting state data from ds002799
with an approach similar to that used in the cluster failure paper.

## Getting the data for 2 subjects

To run from `model-zoo/exhibits/ds2799/`:

model-zoo/exhibits/ds2799/ds002799/derivatives/fmriprep

```bash
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29[2-4]/ses-*/func/*tsv -J 12
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29[2-4]/ses-*/func/*json -J 12
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29[2-4]/ses-*/func/*task-rest*MNI*desc-preproc*bold.nii.gz -J 12
datalad get -d ds002799 ds002799/derivatives/fmriprep/sub-29[2-4]/ses-*/func/*task-rest*MNI*mask.nii.gz -J 12
```

## Running the analysis

```bash
sourcedata=$PWD
output_dir=$PWD/derivatives
tmp_dir=$PWD/tmp

model_file=model-ds000114_desc-testRetestVerbal_smdl.json

mkdir -p ${tmp_dir} ${output_dir}

docker run --rm -it \
    -v ${sourcedata}:/sourcedata \
    -v ${tmp_dir}:/scratch \
    -v ${output_dir}:/output \
        poldracklab/fitlins:0.11.0 \
            --verbose \
            --model /sourcedata/${model_file} \
            -d /sourcedata/ds002799 \
            --work-dir /scratch \
            --participant-label 01 02 \
            --space MNI152NLin2009cAsym \
            --desc-label preproc \
            --estimator nilearn \
            --drift-model cosine \
            --smoothing 6:run:iso \
            /sourcedata/ds000114 /output run
```