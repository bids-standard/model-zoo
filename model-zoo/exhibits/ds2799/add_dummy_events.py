"""This script will add a single events.tsv in the root of a BIDS dataset.

The events.tsv file will 'simulate' a single condition
for the rest task.

This can then be used to run GLM on the resting state data,
to see how many false positives we get.

ASSUMPTIONS:

- all resting state runs have the same number of volumes
- all resting state runs have the same repetition time
"""

import pandas as pd
from pathlib import Path

output_file = Path(__file__).parent / "ds002799" / "task-rest_events.tsv"

# hard coded values that should be adapted to the dataset or run
# TODO get those values dynamically from the dataset.
repetitions_time = 2
nb_vol = 180

# parameters
# adapting thos can allow to test different (slow event vs fast event),
# short block vs long block, etc.
EVENT_DURATION = 10
ISI = 10

onsets = range(0, nb_vol * repetitions_time, EVENT_DURATION + ISI)
durations = [EVENT_DURATION] * len(onsets)
trial_type = ["dummy"] * len(onsets)

df = pd.DataFrame({"onset": onsets, "duration": durations, "trial_type": trial_type})

df.to_csv(output_file, sep="\t", index=False)
