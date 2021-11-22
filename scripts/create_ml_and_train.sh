#!/bin/bash

DATA_PATH=$1

#. env/bin/activate

echo "- Create ML Dataset"
python3 src/usecase/create_ml_dataset.py \
	--input-folder ${DATA_PATH}/cons-v0_6 \
	--output-folder ${DATA_PATH}/ml_dataset

echo "- Train model."
python3 src/usecase/train_model.py \
	--ml-dataset-path ${DATA_PATH}/ml_dataset/df_ml.csv
