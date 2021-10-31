#!/bin/bash
# Copyright (C) 2021  The AURA developers
# See the AUTHORS file at the top-level directory of this distribution
# SPDX-License-Identifier: EPL-2.0

# QRS_DETECTORS=("gqrs" "xqrs" "hamilton" "engelsee" "swt")
QRS_DETECTORS=("hamilton")

## Option - select input directory to be copied from and output directory to copy into
while getopts ":i:a:o:" option; do
    case "${option}" in
	i) file_edf=${OPTARG};;
	a) file_anno=${OPTARG};;
	o) dir_out=${OPTARG};;
    esac
done

dir_script=$(dirname "$0")
LOG=$dir_out/process_directory_$(date +"%Y%m%d-%H%M%S").log

# Check script input integrity
if [[ $file_edf ]] || [[ $file_anno ]] || [[ $dir_out ]]; then
  echo "Start Executing script"
else
  echo "No Input files: $file_edf or Target file: $file_out, use -i,-o options" >&2
  exit 1
fi

echo "* Working on files:" | tee -a $LOG
echo "- EDF file [$file_edf]" | tee -a $LOG
echo "- Anno file [$file_anno]" | tee -a $LOG
echo "- Out dir [$dir_out]" | tee -a $LOG

# Create dir_out if needed
mkdir -p $dir_out

# Get file name without extension
edf_name="$(basename "$edf_file")"
base_name=${edf_name%.edf}

# Extract rr-intervals.
file_out_ecg="${dir_out}/ecg_${base_name}.json"
python3 ${dir_script}/aura_ecg_detector.py \
	-i $edf_file \
	-o $file_out_ecg >> $LOG 2>&1
if [ $? -eq 0 ]; then
      echo "- Out ECG $file_out_ecg - OK" | tee -a $LOG
    else
      echo "- Out ECG $file_out_ecg - Fail" | tee -a $LOG
    fi

# Extract annotations.
file_out_annot="${dir_out}/annot_${base_name}.json"
python3 ${dir_script}/aura_annotation_extractor.py \
	-a $file_anno \
	-o $file_out_annot >> $LOG 2>&1
if [ $? -eq 0 ]; then
    echo "- Out ANNOT $file_out_annot - OK" | tee -a $LOG
else
    echo "- Out ANNOT $file_out_annot - Fail" | tee -a $LOG
fi

# Extract features.
for qrs_detector in ${QRS_DETECTORS[@]}; do
    file_out_feats="${dir_out}/feats_${qrs_detector}_${base_name}.json"
    python3 script/aura_features_computation.py \
	    -i $file_out_ecg \
	    -a $file_out_annot \
	    -o $file_out_feats \
	    -q $qrs_detector >> $LOG 2>&1
    if [ $? -eq 0 ]; then
	echo "- Out FEATS $file_out_feats - OK" | tee -a $LOG
    else
	echo "- Out FEATS $file_out_feats - Fail" | tee -a $LOG
    fi
done

exit 0
