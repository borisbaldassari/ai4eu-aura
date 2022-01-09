#!/bin/bash

# Copyright (C) 2021 The AURA developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-2.0

DATA_PATH=$1
OUT_PATH=$2

mkdir -p ${OUT_PATH}/ml_dataset
mkdir -p ${OUT_PATH}/model

echo "# Create ML Dataset"
echo "  - Data ${DATA_PATH}/cons-v0_6"
echo "  - ML Dataset ${DATA_PATH}/ml_dataset"
echo "  - Model ${DATA_PATH}/ml_dataset"

python3 src/usecase/create_ml_dataset.py \
	--input-folder ${DATA_PATH}/cons-v0_6 \
	--output-folder ${OUT_PATH}/ml_dataset

echo "- Train model."
python3 src/usecase/train_model.py \
	--ml-dataset-path ${OUT_PATH}/ml_dataset/df_ml.csv \
	--output-folder ${OUT_PATH}/model
