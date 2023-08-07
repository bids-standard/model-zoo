# Compare sessions

## Getting the data for 2 subjects

To run from `model-zoo/exhibits/ds000114`:

```bash
datalad get -d ds000114-fmriprep ds000114-fmriprep/sub-0[1-2]/ses-*/func/*tsv -J 12
datalad get -d ds000114-fmriprep ds000114-fmriprep/sub-0[1-2]/ses-*/func/*json -J 12
datalad get -d ds000114-fmriprep ds000114-fmriprep/sub-0[1-2]/ses-*/func/*MNI*desc-preproc*bold.nii.gz -J 12
datalad get -d ds000114-fmriprep ds000114-fmriprep/sub-0[1-2]/ses-*/func/*MNI*mask.nii.gz -J 12
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
            -d /sourcedata/ds000114-fmriprep \
            --work-dir /scratch \
            --participant-label 01 02 \
            --space MNI152NLin2009cAsym \
            --desc-label preproc \
            --estimator nilearn \
            --drift-model cosine \
            --smoothing 6:run:iso \
            /sourcedata/ds000114 /output run
```

## Issues

- Cannot have Description in the model.
- Images do not show when using docker to run the analysis: the path to the image is relative to the container, not the host.
