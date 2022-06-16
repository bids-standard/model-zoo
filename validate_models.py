from pathlib import Path
from bsmschema.models import BIDSStatsModel
from pydantic import ValidationError
import sys

all_models = Path('.').glob('*/*smdl.json')
status = 0
for i in all_models:
    status = '✓'
    try:
        BIDSStatsModel.parse_file(str(i))
    except ValidationError as e:
       print(f"Model: {i.absolute()}, errors ❌")
       print(e)
       status = 1
    else:
        print(f"Model: {i.absolute()}, passed ✓")


sys.exit(status)

