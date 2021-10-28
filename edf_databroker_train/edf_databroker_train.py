import grpc
from concurrent import futures
#from typing import List
import time
import edf_databroker_train_pb2 as pb2
import edf_databroker_train_pb2_grpc as pb2_grpc
import glob
import os
from pathlib import Path

# gRPC port
port = 8061

data_path="data/"
edf_files: list = []

class EdfDatabroker(pb2_grpc.EdfDatabrokerServicer):

    def __init__(self):
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if file.endswith('.edf'):
#                    print(f"- file {os.path.join(root, file)}.")
                    edf_files.append(f"{os.path.join(root, file)}")
        self.edf_files = edf_files

    def get_next_edf_file(self, request, context):
        response = pb2.EdfText()
        if len(self.edf_files) == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("All data has been processed")
            exit(0)
        else:
            edf_file = self.edf_files[0]
            response.edf = edf_file
            anno_file = os.path.splitext(edf_file)[0]+'.tse_bi'
            response.anno = anno_file
            self.edf_files.pop(0)
        return response

# broker = EdfDatabroker()
# edf_file = broker.get_next_file()
# print(f"Edf File is {edf_file}")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
pb2_grpc.add_EdfDatabrokerServicer_to_server(EdfDatabroker(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
