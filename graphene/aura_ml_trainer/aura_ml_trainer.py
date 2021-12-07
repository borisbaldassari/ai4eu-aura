import grpc
from concurrent import futures
import time
import aura_ml_trainer_pb2 as pb2
import aura_ml_trainer_pb2_grpc as pb2_grpc
import os
import re
import subprocess

# gRPC port
port = 8061

data_path = ""
model_path = ""


class AuraMlTrainer(pb2_grpc.AuraMlTrainerServicer):
    def __init__(self):
        print("Initialising AuraMlTrainer.")
        data_path_abs = os.environ['SHARED_FOLDER_PATH']
        print(f"  - volume path [{data_path_abs}].")
        self.data_path = f"{data_path_abs}/out"
        self.model_path = f"{data_path_abs}/model"

    def startTraining(self, request, context):
        response = pb2.TrainingStatus()
        print(f"\n* in aura_ml_trainer/startTraining {response}.")
        dir_in = request.dir
        dir_data = f"{self.data_path}{dir_in}"
        print("In aura_ml_trainer.py:")
        print(f"- data_path {self.data_path}")
        print(f"- dir_data {dir_data}")
        print(f"- model_path {self.model_path}")
        file_list=os.listdir(dir_data)
        print(f"file list {file_list}")
        subprocess.call(
            [
                "bash",
                "/aura/scripts/create_ml_and_train.sh",
                dir_data,
                self.model_path,
            ]
        )
        response.accuracy = 0.2
        response.validation_loss = 0.1
        response.status_text = "ok"
        print("* In aura_ml_trainer/startTraining")
        print(f"{response}.")
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
pb2_grpc.add_AuraMlTrainerServicer_to_server(AuraMlTrainer(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except grpc.RpcError:
    server.stop(0)
