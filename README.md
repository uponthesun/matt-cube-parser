# Requires
Python (Wrote this using Python 3, may work with Python 2, but haven't tested it.)

# Usage
From Linux / Mac terminal, or Windows command prompt, run:
```
python convert_mse.py input_file.csv
```

* input_file.csv should be an input file in the format of Matt's custom cube spreadsheet, exported as csv.
* The output of the script is two files:
  * output.mse-set - Magic Set Editor file.
  * failed.txt - Text file containing the input lines which failed to be parsed, likely because of being
improperly formatted, or possibly because of a bug in the script.