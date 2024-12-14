# #!/bin/bash

# dt=$(date +%Y)
# FILE=../archived/raw/raw_data_$dt.csv

# if test -f "$FILE"; then
#     echo "$FILE exists. Launching integration"
# else 
#     echo "Downloading data"
#     cd ../data_collector/bin
#     bash get_data.sh
#     echo "Data downloaded"
#     cd ..
# fi

# echo "Integrating data"
# cd ../data_integrator/bin
# bash workflow.sh
# echo "Data integrated"

# echo "Processing data"
# cd ../../data_processor/bin
# bash workflow.sh
# echo "Processing data succeeded"

# cd ../bin

#!/bin/bash

dt=$(date +%Y)
FILE=../raw_data_$dt.csv

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

start_time=$(date +%s)

log_message "Starting data pipeline..."

if test -f "$FILE"; then
    log_message "$FILE exists. Launching integration..."
else
    log_message "No raw data file detected. Downloading data..."
    cd ../data_collector/bin || exit
    bash get_data.sh
    if [ $? -ne 0 ]; then
        log_message "Error downloading data. Exiting."
        exit 1
    fi
    log_message "Data downloaded successfully."
    cd .. || exit
fi

echo "Integrating data"
cd ../data_integrator/bin || exit
bash workflow.sh | tee ../../log/integration.log
if [ $? -ne 0 ]; then
    echo "Error during data integration. Check log/integration.log for details."
    exit 1
fi
echo "Data integrated"


log_message "Processing data..."
cd ../../data_processor/bin || exit
bash workflow.sh
if [ $? -ne 0 ]; then
    log_message "Error during data processing. Exiting."
    exit 1
fi
log_message "Data processing succeeded."

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))

log_message "Data pipeline completed successfully in $elapsed_time seconds."
cd ../bin || exit
