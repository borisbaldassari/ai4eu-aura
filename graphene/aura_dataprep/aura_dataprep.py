# Copyright (C) 2021 The AURA developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-2.0

import grpc
from concurrent import futures
import time
import aura_dataprep_pb2 as pb2
import aura_dataprep_pb2_grpc as pb2_grpc
import os
import re
import subprocess

# gRPC port
port = 8061

edf_path_rel = "tuh/"
data_path_rel = "out/"

edf_path = ""
data_path = ""


class AuraDataprep(pb2_grpc.AuraDataprepServicer):
    def __init__(self):
        print("Initialising AuraDataprep.")
        data_path_abs = os.environ['SHARED_FOLDER_PATH']
        print(f"  - volume path [{data_path_abs}].")
        self.edf_path = f"{data_path_abs}/{edf_path_rel}"
        self.data_path = f"{data_path_abs}/{data_path_rel}"

    def prepareEdfDir(self, request, context):
        response = pb2.OutDir()
        dir_in = request.dir
        dir_edf = f"{self.edf_path}{dir_in}"
        print("In aura_dataprep.py:")
        print(f"- dir_edf {dir_edf}")
        print(f"- data_path {self.data_path}")
        print(f"- dir_in {dir_in}")
        subprocess.call(
            [
                "bash",
                "/aura/scripts/run_bash_pipeline.sh",
                dir_edf,
                self.data_path,
                dir_in,
            ]
        )
        response.dir = "false"
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
pb2_grpc.add_AuraDataprepServicer_to_server(AuraDataprep(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except grpc.RpcError:
    server.stop(0)
