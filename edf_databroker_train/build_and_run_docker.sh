
# This script builds the Docker image with the corresponding
# gRPC scripts, runs it and start listening on port 8061.

docker build . -t bbaldassari/edf_databroker_train
docker run -p 8061:8061 bbaldassari/edf_databroker_train

