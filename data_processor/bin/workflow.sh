#!/bin/bash

dt=$(date +%Y)

STAGED_FILE=../../archived/staged/staged_data_$dt.csv

if test -f "$STAGED_FILE"; then
  echo "$STAGED_FILE exists. Launching data processing"
  bash run.sh
  echo "Data processing succeeded"
else
  echo "No staged file detected"
fi