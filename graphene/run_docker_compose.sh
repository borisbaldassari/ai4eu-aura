#!/bin/bash

DATA_DIR=$1
SCRIPT=$(basename $0)
if [ -z  "$DATA_DIR" ]; then
    echo "Usage: $0 /data/dir"
    exit
fi
export DATA_DIR
echo "# Using [$DATA_DIR] as data dir."

docker-compose -f docker-compose-dataprep.yml up
docker-compose -f docker-compose-mltrain.yml up
