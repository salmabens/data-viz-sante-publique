#!/bin/bash

dt=$(date +%Y)
FILE=../../raw_data_$dt.csv

if test -f "$FILE"; then
  echo "$FILE exists. Launching integration"
  bash run.sh
  echo "Data integration succeeded"
  cp -f $FILE ../../archived/raw/raw_data_$dt.csv
else
  echo "No raw file detected"
fi
