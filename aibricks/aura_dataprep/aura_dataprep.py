import grpc
from concurrent import futures
import time
import aura_dataprep_pb2 as pb2
import aura_dataprep_pb2_grpc as pb2_grpc
import os
import re
import subprocess
from pathlib import Path

# gRPC port
port = 8061

edf_path="/data/edf/"
data_path="/data/out/"
#edf_files: list = []

class AuraDataprep(pb2_grpc.AuraDataprepServicer):

    def __init__(self):
        print("Initialising AuraDataprep.")
        #        self.edf_files = edf_files

    def prepareEdfFile(self, request, context):
        response = pb2.DataFile()
        file_edf = request.edf
        file_anno = request.anno
        dir_edf = os.path.dirname(file_edf)
        #dir_rel = dir_edf.removeprefix(edf_path)
        dir_out = re.sub('^' + edf_path, data_path, dir_edf)
        #dir_out = f"{data_path}/{dir_rel}"
        subprocess.call(["bash",
                         "./scripts/aura_clean_process_file.sh",
                         "-i", file_edf,
                         "-a", file_anno,
                         "-o", dir_out,
        ])

        base_name = os.path.basename(file_edf)
        response.ecg = f"{dir_out}/ecg_{base_name}.json"
        response.anno = f"{dir_out}/anno_{base_name}.json"
        response.feats = f"{dir_out}/feats_hamilton_{base_name}.json"
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
pb2_grpc.add_AuraDataprepServicer_to_server(AuraDataprep(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except:
    server.stop(0)
