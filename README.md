
# AURA Epileptic Seizure Detection

This repository contains everything required to run the AURA Seizure detection ML process on ECGs.

It notably features:
* Pipelines for data cleaning and preparation, model training, prediction and visualisation.
* An Airflow orchestration setup to run the various pipelines locally via a local executor.
* An [AIBricks](https://ai4europe.eu) orchestration setup to run the pipelines in a kubernetes cluster.


## Introduction


### AURA

Aura is a not-for-profit organisation working on epileptic seizure detection.

The AURA workflow basically relies on a RandomForest Machine Learning model to detect epileptic seizures from ECGs data.


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


## Running with Airflow



## Running with AIBricks

See [README.md](aibricks/README.md) in `aibricks/`.


## Contributing

We try to keep the repository clean and well maintained. 

Pull Requests shall be accepted only if:

* The feature works and has been tested on a CI system.
* There are tests to run the new code. Tests must be reproducible and automated as much as possible.
* Python code follows the default configuration of flake8.
* Documentation is present and current. If a new feature is introduced it must be documented, and for a change to an existing feature the current documentation must be updated.

We use Travis for all Python code, and container-based tests are executed on a [Jenkins instance](https://art.castalia.camp/).



