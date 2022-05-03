#!/bin/bash

dataset_root="$(pwd)"

bids_dir=${dataset_root}/sourcedata/raw
fmriprep_dir=${dataset_root}/sourcedata/fmriprep
output_dir=${dataset_root}/derivatives
tmp_dir=${dataset_root}/tmp
model_dir=${dataset_root}/sourcedata/model/spm_tutorials

model_file=spm-MoAE_smdl.json

mkdir -p ${tmp_dir} ${output_dir}

fitlins --participant-label 01 \
    -m ${model_dir}/${model_file} \
    -d ${fmriprep_dir} \
    -w ${tmp_dir} \
    --space MNI152NLin6Asym \
    --desc-label preproc \
    --estimator nistats \
    --drift-model cosine \
    --smoothing 6:run:iso \
    ${bids_dir} ${output_dir} run
