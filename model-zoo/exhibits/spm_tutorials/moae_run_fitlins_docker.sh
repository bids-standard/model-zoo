#!/bin/bash

this_dir="$(pwd)"

sourcedata=${this_dir}
derivatives=${this_dir}/derivatives/moae
tmp_dir=${this_dir}/tmp

model_file=model-MoAE-desc-fitlins_smdl.json

mkdir -p ${derivatives}
mkdir -p ${tmp_dir}

docker run --rm -it \
    -v ${sourcedata}:/sourcedata:ro \
    -v ${derivatives}:/out \
    -v ${tmp_dir}:/scratch \
    poldracklab/fitlins:0.10.1 \
    -v \
    -m /sourcedata/${model_file} \
    -d /sourcedata/moae_fmriprep \
    -w /scratch \
    --participant-label 01 \
    --space MNI152NLin6Asym \
    --desc-label preproc \
    --estimator nistats \
    --drift-model cosine \
    --smoothing 6:run:iso \
    /sourcedata/moae_raw /out run
