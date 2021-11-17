#!/bin/bash
# This script builds the Docker image with the corresponding
# gRPC scripts, runs it and start listening on port 8061.

IMAGE="bbaldassari/aura_dataprep"

echo "* Prepare directories & scripts."
rm -rf data scripts src
cp -r ../../data/ ../../scripts/ ../../src/ ./

. ../env/bin/activate
python -m grpc_tools.protoc -I=./ --python_out=. --grpc_python_out=. aura_dataprep.proto

echo "* Build Docker image."
docker build . -t $IMAGE 

echo "* Clean temp files."
#rm -rf data/ scripts/ src/

echo "* Checking if a previous Docker image is running."
docker_id=$(docker ps | grep $IMAGE | cut -f1 -d\ )
if [[ $docker_id != "" ]]; then
    echo "  - Stop running Docker image $docker_id."
    docker stop $docker_id
else
    echo "  - Found no docker image."
    echo "    Listing $IMAGE:"
    docker ps | grep $IMAGE
fi

echo "* Run Docker image."
docker run -p 8061:8061 -e SHARED_FOLDER_PATH="/data/" -v $(pwd)/data:/data/ $IMAGE &
sleep 2

echo "* Run client python test script."
source ../env/bin/activate
pytest test_aura_dataprep.py
pytest_result=$?

echo "* Stop the Docker image."
docker_id=$(docker ps | grep $IMAGE | cut -f1 -d\ )
if [[ $docker_id != "" ]]; then
    echo "  - Stop running Docker image $docker_id."
    docker stop $docker_id
else
    echo "  - Found no docker image."
    echo "    Listing $IMAGE:"
    docker ps | grep $IMAGE
    docker ps | grep $IMAGE | cut -f1 -d\ 
fi

exit $pytest_result
