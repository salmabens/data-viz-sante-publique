#!/bin/bash

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}


if [ ! -d "../log" ]; then
    mkdir -p ../log
    log_message "Created log directory"
fi


log_message "Starting installation..."
(cd ../ && log_message "Running install.sh..." && bash install.sh | tee log/install.log)
if [ $? -ne 0 ]; then
    log_message "Error during installation. Check log/install.log for details."
    exit 1
fi
log_message "Installation completed."


log_message "Starting data pipeline..."
(cd . && log_message "Running launch.sh..." && bash launch.sh | tee ../log/data_pipeline.log)
if [ $? -ne 0 ]; then
    log_message "Error during data pipeline. Check log/data_pipeline.log for details."
    exit 1
fi
log_message "Data pipeline completed."


log_message "Starting web application..."
(cd ../webapp/bin && log_message "Running webapp launch.sh..." && bash launch.sh | tee ../../log/webapp.log)
if [ $? -ne 0 ]; then
    log_message "Error during web application launch. Check log/webapp.log for details."
    exit 1
fi
log_message "Web application launch completed."

log_message "All steps completed successfully!"
