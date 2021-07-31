# BIDS stats model for SPM data sets

These models are meant to correspond to the stats model of used in the SPM
manual.

Datasets and corresponding sections of the SPM manuals are available from here:
https://www.fil.ion.ucl.ac.uk/spm/data/

## Mother of all experiments (MoAE)

Simple block design: one subject, one run, one condition.

BIDS dataset available from:
https://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.bids.zip

## Face repetition priming

Event related design: : one subject, one run, 2 X 2 design.

There is no BIDS dataset available so we provide an Matlab / Octave script to
download and convert the data set (`spm_tutorials/download_convert_face_rep_ds.m`)
taken from [cpp_spm](https://github.com/cpp-lln-lab/CPP_SPM).
