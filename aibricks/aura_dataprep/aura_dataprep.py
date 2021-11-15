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

edf_path = "/data_in/"
data_path = "/data_out/"
# edf_files: list = []


class AuraDataprep(pb2_grpc.AuraDataprepServicer):
    def __init__(self):
        print("Initialising AuraDataprep.")
        #        self.edf_files = edf_files

    def prepareEdfDir(self, request, context):
        response = pb2.OutDir()
        dir_in = request.dir
        dir_edf = f"{edf_path}{dir_in}"
        print("In aura_dataprep.py:")
        print(f"- dir_edf {dir_edf}")
#        dir_out = f"{data_path}{dir_in}"
#        print(f"- dir_out {dir_out}")
        subprocess.call(
            [
                "bash",
                "/aura/scripts/run_bash_pipeline.sh",
                dir_edf,
                data_path,
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
