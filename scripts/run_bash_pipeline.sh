
# this script is meant to be executed from the root directory of the repo.

DATA_PATH=$1
EXPORT_PATH=$2

FOLDER_PATH=$(pwd)
SRC_PATH=./src
TEST_PATH=./tests

mkdir -p $EXPORT_PATH

echo "- Detect rr-intervals."
./scripts/bash_pipeline/1_detect_qrs_wrapper.sh  -i ${DATA_PATH} -o ${EXPORT_PATH}/res-v0_6

echo "- Compute features."
./scripts/bash_pipeline/2_compute_hrvanalysis_features_wrapper.sh  -i ${EXPORT_PATH}/res-v0_6 -o ${EXPORT_PATH}/feats-v0_6

echo "- Consolidate features and annotations."
./scripts/bash_pipeline/3_consolidate_feats_and_annot_wrapper.sh  -i ${EXPORT_PATH}/feats-v0_6 -a ${DATA_PATH} -o ${EXPORT_PATH}/cons-v0_6

echo "Done"

