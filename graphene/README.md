
% Containers for AURA

Implementation of the AURA workflow for [Eclipse Graphene](https://eclipse.org/graphene).


## Workflows

We built two separate workflows to:
* The first workflow trains the model with a dedicated training data set to learn seizures detection. It takes as input EDF files (ECGs), prepare data files and train the model, then save the trained model.
* The second workflow takes a different data set, and from the model trained previously predicts seizures on the ECG files. ECG files are then imported with the predicted seizure annotations into an InfluxDB database and displayed using Grafana.

We also provide two different ways to run the containers: 
* Using Eclipse Graphene as a powerful visual editor and orchestrator.
* Using docker-compose for simple setups.


### Model training

![AI4EU_AURA_trainer.png](https://files.nuclino.com/files/b909ba0e-eb25-459e-af44-6f2e55a58f1c/AI4EU_AURA_trainer.png)

The outcome of this workflow is an artefact representing the trained model, that will be re-onboarded into the Graphene platform to enable further reuse as an easy-to-deploy visual block.


### Prediction

![AI4EU_AURA_predictor.png](https://files.nuclino.com/files/a5e6b5af-8376-4faf-a7e0-05ed65fe3c75/AI4EU_AURA_predictor.png)

The visualisation block displays the ECGs with both the model predictions and the original annotations so practitioners can visually compare the model's performance. 


## Execution using docker-compose

The docker-compose setup makes use of the Docker images for the execution. To run the full process, make sure that the EDF files are stored in a subdirectory `tuh/` of the data dir, e.g. `data/tuh` and then simply execute:

```
$ bash run_docker_compose.sh ../data/
```

The two steps can also be executed on their own. One need to set the `DATA_DIR` env variable to point to the data directory. So when in the `graphene/` directory, issue the following commands:

```
$ export DATA_DIR=../data/
$ docker-compose -f docker-compose-dataprep.yml up
```

and then:

```
$ docker-compose -f docker-compose-mltrain.yml up
```


## Execution using Eclipse Graphene

All images are built along the same structure and provide the same facilities for testing. We'll use image `edf_databroker_train` as an example, but any image directory name can be used interchangeably.


## Containers

### Data cleaner

Dockerfile and scripts are located in `datacleaner/`. This image runs the data preparation steps for a directory.
A set of data samples is provided


#### Sequence:

Search for all `.edf` files within the input directory, and for each file run:
  - the ecg detector (`aura_ecg_detector.py`),
  - the annotation extractor (`aura_annotation_extractor.py`),
  - the feature extraction (`aura_features_computation.py`).


## Build and run the images

### Local setup

Open up a terminal in the image directory to run the server, and execute the following command:
```
source env/bin/activate
python aura_dataprep.py
```

Open another terminal in the image directory for the client execution, and execute the following command:
```
source env/bin/activate
pytest aura_dataprep.py
```


### Testing Docker images

One can test the Docker images with the following commands:

```
bash build_and_run_docker.sh
```

Commands to build and run a container manually:

```
docker build . -t bbaldassari/aura_dataprep
docker run -p 8061:8061 bbaldassari/aura_dataprep
```


#### Building and Testing dataprep

The image is based off a python image and embeds the scripts to clean the data. It is self-sufficient.

Build the image. In the `aura_dataprep` directory, run:

```
docker build . -t bbaldassari/aura_dataprep
```

Run the image. For a test drive, you can use the default data sample found in `test/data`:

```
docker run -v $(pwd)/data/:/data bbaldassari/aura_dataprep bash /aura/scripts/run_bash_pipeline.sh /data/tuh /data/out
```

All exports will be stored, in this example, in the `data/out/` local directory.

Example:

```
$ docker run -v $(pwd)/data/:/data bbaldassari/aura_dataprep bash /aura/scripts/run_bash_pipeline.sh /data/tuh /data/out
# Run dataprep pipeline - In /data/tuh - Out 
- Detect rr-intervals.
Start Executing script
/aura
/data/tuh/dev/01_tcp_ar/002/00009578/00009578_s006_t001.edf - OK
/data/tuh/dev/01_tcp_ar/002/00009578/00009578_s002_t001.edf - OK
- Compute features.
Start Executing script
/aura
/data/out/res-v0_6//dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv # - OK
/data/out/res-v0_6//dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv # - OK
- Consolidate features and annotations.
Start Executing script
/aura
/data/out/feats-v0_6//dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv and /data/tuh/dev/01_tcp_ar/002/00009578/00009578_s002_t001.tse_bi # - OK
/data/out/feats-v0_6//dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv and /data/tuh/dev/01_tcp_ar/002/00009578/00009578_s006_t001.tse_bi # - OK
Done

```


#### Building and testing ml_trainer

The same applies to the ml_trainer image. To execute the training use the following command line:

```
docker run -v $(pwd)/data/:/data bbaldassari/aura_ml_trainer bash /aura/scripts/create_ml_and_train.sh /data/out /data/model
```


