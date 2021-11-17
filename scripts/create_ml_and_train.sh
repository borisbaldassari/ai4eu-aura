#!/bin/bash

. env/bin/activate
python3 src/usecase/create_ml_dataset.py --input-folder output/cons-v0_6 --output-folder output/ml_dataset
python3 src/usecase/train_model.py --ml-dataset-path output/ml_dataset/df_ml.csv