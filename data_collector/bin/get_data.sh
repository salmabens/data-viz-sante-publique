#!/bin/bash
source ../conf/collector.conf

echo "The API URL is set as: ${api_url}"
echo "Target path is set as: ${target_path}"

dt=2024
curl -XGET ${api_url} > ${target_path}/raw_data_$dt.csv



