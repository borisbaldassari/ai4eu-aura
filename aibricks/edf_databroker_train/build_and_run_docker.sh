#!/bin/bash
# This script builds the Docker image with the corresponding
# gRPC scripts, runs it and start listening on port 8061.

echo "* Build Docker image."
docker build . -t bbaldassari/edf_databroker_train --no-cache

echo "* Checking if a previous Docker image is running."
docker_id=$(docker ps | grep edf_databroker_train | cut -f1 -d\ )
if [[ $docker_id != "" ]]; then
    echo "  - Stop running Docker image $docker_id."
    docker stop $docker_id
else
    echo "  - Found no docker image."
    echo "    Listing edf_databroker_train:"
    docker ps | grep edf_databroker_train
    docker ps | grep edf_databroker_train | cut -f1 -d\ 
fi

echo "* Run Docker image."
docker run -p 8061:8061 bbaldassari/edf_databroker_train &

echo "* Run client python test script."
source ../env/bin/activate
pytest test_edf_databroker_train.py
pytest_result=$?

echo "* Stop the Docker image."
docker_id=$(docker ps | grep edf_databroker_train | cut -f1 -d\ )
if [[ $docker_id != "" ]]; then
    echo "  - Stop running Docker image $docker_id."
    docker stop $docker_id
else
    echo "  - Found no docker image."
    echo "    Listing edf_databroker_train:"
    docker ps | grep edf_databroker_train
    docker ps | grep edf_databroker_train | cut -f1 -d\ 
fi

exit $pytest_result
