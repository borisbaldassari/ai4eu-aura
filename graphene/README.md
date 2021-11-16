
# AURA on AIBricks

Implementation of the AURA workflow for AIBricks.


## Workflows

We built two separate workflows to:
* The first workflow trains the model with a dedicated training data set to learn seizures detection. It takes as input EDF files (ECGs), prepare data files and train the model, then save the trained model.
* The second workflow takes a different data set, and from the model trained previously predicts seizures on the ECG files. ECG files are then imported with the predicted seizure annotations into an InfluxDB database and displayed using Grafana.


### Model training

![AI4EU_AURA_trainer.png](https://files.nuclino.com/files/b909ba0e-eb25-459e-af44-6f2e55a58f1c/AI4EU_AURA_trainer.png)

The outcome of this workflow is an artefact representing the trained model, that will be re-onboarded into the AIBricks platform to enable further reuse as an easy-to-deploy visual block.


### Prediction

![AI4EU_AURA_predictor.png](https://files.nuclino.com/files/a5e6b5af-8376-4faf-a7e0-05ed65fe3c75/AI4EU_AURA_predictor.png)

The visualisation block displays the ECGs with both the model predictions and the original annotations so practitioners can visually compare the model's performance. 


## Execution and tests

All images are built along the same structure and provide the same facilities for testing. We'll use image `edf_databroker_train` as an example, but any image directory name can be used interchangeably.


### Testing scripts

Open up a terminal in the image directory to run the server, and execute the following command:
```
source env/bin/activate
python edf_databroker_train.py
```

Open another terminal in the image directory for the client execution, and execute the following command:
```
source env/bin/activate
pytest test_edf_databroker_train.py
```


### Testing Docker images

One can test the Docker images with the following commands:
```
bash build_and_run_docker.sh
```

## Containers

Commands to build and run a container:

```
docker build . -t bbaldassari/edf_databroker_train
docker run -p 8061:8061 bbaldassari/edf_databroker_train
```

### Data cleaner

Dockerfile and scripts are located in `datacleaner/`. This image runs the data preparation steps for a directory.
A set of data samples is provided


#### Sequence:

Search for all `.edf` files within the input directory, and for each file run:
  - the ecg detector (`aura_ecg_detector.py`),
  - the annotation extractor (`aura_annotation_extractor.py`),
  - the feature extraction (`aura_features_computation.py`).


#### Building and Testing

The image is based off a python image and embeds the scripts to clean the data. It is self-sufficient.

Build the image. In the `aura_dataprep` directory, run:

```
docker build . -t bbaldassari/aura_dataprep
```

Run the image. For a test drive, you can use the default data sample found in `test/data`:

```
docker run -v $(pwd)/data/tuh/:/data_in -v $(pwd)/export/:/data_out bbaldassari/aura_dataprep bash /aura/scripts/run_bash_pipeline.sh /data_in /data_out
```

All exports will be stored, in this example, in the `export/` local directory.

Example:

```
boris@castalia:aura_dataprep$ docker run -v $(pwd)/data/tuh/:/data_in -v $(pwd)/export/:/data_out bbaldassari/aura_dataprep bash /aura/scripts/run_bash_pipeline.sh /data_in /data_out
- Detect rr-intervals.
Start Executing script
/aura
/data_in//dev/01_tcp_ar/002/00009578/00009578_s006_t001.edf - OK
/data_in//dev/01_tcp_ar/002/00009578/00009578_s002_t001.edf - OK
- Compute features.
Start Executing script
/aura
/data_out//res-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv # - OK
/data_out//res-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv # - OK
- Consolidate features and annotations.
Start Executing script
/aura
/data_in//dev/01_tcp_ar/002/00009578/00009578_s002_t001.tse_bi
/data_out//feats-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv and /data_in//dev/01_tcp_ar/002/00009578/00009578_s002_t001.tse_bi # - OK
/data_in//dev/01_tcp_ar/002/00009578/00009578_s006_t001.tse_bi
/data_out//feats-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv and /data_in//dev/01_tcp_ar/002/00009578/00009578_s006_t001.tse_bi # - OK
Done
boris@castalia:aura_dataprep$ 
```

