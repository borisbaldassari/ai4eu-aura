#!/bin/bash
# Copyright (C) 2021  The AURA developers
# See the AUTHORS file at the top-level directory of this distribution
# SPDX-License-Identifier: EPL-2.0

# QRS_DETECTORS=("gqrs" "xqrs" "hamilton" "engelsee" "swt")
QRS_DETECTORS=("hamilton")

## Option - select input directory to be copied from and output directory to copy into
while getopts ":i:o:" option; do
    case "${option}" in
	i) dir_edf=${OPTARG};;
	o) dir_out=${OPTARG};;
    esac
done

dir_script=$(dirname "$0")
LOG=$dir_out/process_directory_$(date +"%Y%m%d-%H%M%S").log

# Check script input integrity
if [[ $dir_edf ]] || [[ $dir_out ]]; then
  echo "Start Executing script"
else
  echo "No Input directory: $dir_edf or Target directory: $dir_out, use -i,-o options" >&2
  exit 1
fi


## List all EDF files in dir_edf ##
for edf_file in $(find $dir_edf/ -type f -name "*.edf" ); do
    echo "* Working on file [$edf_file]" | tee -a $LOG

    # Get file name without extension
    base_name=${edf_file%.edf}
    tse_file="${base_name}.tse_bi"

    # Get relative path and out file name
    path_edf="$(dirname "$edf_file")"
    relative_path="${path_edf#$dir_edf}"
    dir_out_full="${dir_out}/${relative_path}"

    # Create destination directory if it doesn't exist
    mkdir -p -- "$dir_out_full"

    # Execute file cleaning process
    bash aura_clean_process_file.sh -i $edf_file -a $tse_file -o $dir_out_full
done

exit 0
