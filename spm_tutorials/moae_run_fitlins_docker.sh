#!/bin/bash

sourcedata=$(pwd)/sourcedata
derivatives=$(pwd)/derivatives
tmp_dir=$(pwd)/tmp

mkdir -p ${derivatives}
mkdir -p ${tmp_dir}

docker run --rm -it \
    -v ${sourcedata}:/sourcedata:ro \
    -v ${derivatives}:/out \
    -v ${tmp_dir}:/scratch \
    poldracklab/fitlins:0.10.1 \
    -v \
    -m /sourcedata/model/spm_tutorials/spm-MoAE_smdl.json \
    -d /sourcedata/fmriprep \
    -w /scratch \
    --participant-label 01 \
    --drop-missing \
    --space MNI152NLin6Asym \
    --desc-label preproc \
    --estimator nistats \
    --drift-model cosine \
    --smoothing 6:run:iso \
    /sourcedata/raw /out run
