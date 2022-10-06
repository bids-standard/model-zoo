#!/bin/bash

this_dir="$(pwd)"

bids_dir=${this_dir}/facerep_raw
fmriprep_dir=${this_dir}/facerep_fmriprep/derivatives/fmriprep
output_dir=${this_dir}/derivatives/facerep
tmp_dir=${this_dir}/tmp
model_dir=${this_dir}

model_file=model-FaceRep_smdl.json

mkdir -p ${tmp_dir} ${output_dir}

fitlins --participant-label 01 \
    -m ${model_dir}/${model_file} \
    -d ${fmriprep_dir} \
    -w ${tmp_dir} \
    --space MNI152NLin2009cAsym \
    --desc-label preproc \
    --estimator nistats \
    --drift-model cosine \
    --smoothing 6:run:iso \
    ${bids_dir} ${output_dir} run
