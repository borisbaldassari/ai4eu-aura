#!/bin/bash

# Copyright (C) 2021 The AURA developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-2.0


DATA_DIR=$1
SCRIPT=$(basename $0)

if [ -z  "$DATA_DIR" ]; then
    echo "Usage: $SCRIPT /data/dir"
    exit
fi
export DATA_DIR
echo "# Using [$DATA_DIR] as data dir."

docker-compose -f docker-compose-dataprep.yml up
docker-compose -f docker-compose-mltrain.yml up
