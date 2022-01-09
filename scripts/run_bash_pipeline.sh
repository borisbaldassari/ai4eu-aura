
# Copyright (C) 2021 The AURA developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-2.0

# this script is meant to be executed from the root directory of the repo.

DATA_PATH=$1
EXPORT_BASE=$2
EXPORT_PATH=$3

mkdir -p ${EXPORT_BASE}/res-v0_6/${EXPORT_PATH}/
mkdir -p ${EXPORT_BASE}/feats-v0_6/${EXPORT_PATH}/
mkdir -p ${EXPORT_BASE}/cons-v0_6/${EXPORT_PATH}/

echo "# Run dataprep pipeline - In $DATA_PATH - Out $EXPORT_PATH"

echo "- Detect rr-intervals."
./scripts/bash_pipeline/1_detect_qrs_wrapper.sh  \
	-i ${DATA_PATH} \
	-o ${EXPORT_BASE}/res-v0_6/${EXPORT_PATH}

echo "- Compute features."
./scripts/bash_pipeline/2_compute_hrvanalysis_features_wrapper.sh \
	-i ${EXPORT_BASE}/res-v0_6/${EXPORT_PATH} \
	-o ${EXPORT_BASE}/feats-v0_6/${EXPORT_PATH}

echo "- Consolidate features and annotations."
./scripts/bash_pipeline/3_consolidate_feats_and_annot_wrapper.sh  \
	-i ${EXPORT_BASE}/feats-v0_6/${EXPORT_PATH} \
	-a ${DATA_PATH} \
	-o ${EXPORT_BASE}/cons-v0_6/${EXPORT_PATH}

echo "Done"

