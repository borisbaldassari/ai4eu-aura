# Copyright (C) 2021 The AURA developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-2.0

import grpc
import aura_ml_trainer_pb2 as pb2
import aura_ml_trainer_pb2_grpc as pb2_grpc
import time
from typing import List, Any
import os

grpc_url = "localhost:8061"

data_dir_1 = {
    "dir": "",
}

out_status_1 = {
    "accuracy": 0.2,
    "validation_loss": 0.8,
    "status_text": "Done",
}


def get_grpc() -> List[Any]:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = pb2_grpc.AuraMlTrainerStub(channel)
        rep = pb2.TrainingStatus()
        try:
            data_1 = pb2.DataDir(
                dir=data_dir_1["dir"],
            )
            rep = stub.startTraining(data_1)
            print(f"reponse {rep}")
        except grpc.RpcError as rpc_error:
            print(f"gRPC Error: {rpc_error}.")
        return rep


def test_grpc():
    stats = get_grpc()
    assert stats is not None
    print(f"stats is {stats}")
#    print(f"stats[0] is {stats[0]}")
    assert stats.accuracy == out_status_1["accuracy"]
    assert stats.validation_loss == out_status_1["validation_loss"]
    assert stats.status_text == out_status_1["status_text"]
    assert os.path.exists("data/out/cons-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv")
    assert os.path.exists("data/out/cons-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv")
    assert os.path.exists("data/out/res-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv")
    assert os.path.exists("data/out/res-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv")
    assert os.path.exists("data/out/feats-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv")
    assert os.path.exists("data/out/feats-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv")


if __name__ == "__main__":
    print("Executing script:")
    dirs = get_grpc()
    print(f"dirs are {dirs}")
