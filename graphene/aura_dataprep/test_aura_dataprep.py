import grpc
import aura_dataprep_pb2 as pb2
import aura_dataprep_pb2_grpc as pb2_grpc
import time
from typing import List, Any
import os

grpc_url = "localhost:8061"

edf_dir_1 = {
    "dir": "dev/01_tcp_ar/002/00009578/",
}

out_dir_1 = {
    "dir": "false",
#    "dir": "tuh/dev/01_tcp_ar/002/00009578/",
}


def get_grpc() -> List[Any]:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = pb2_grpc.AuraDataprepStub(channel)
        rep: List[Any] = []
        try:
            edf_1 = pb2.EdfDir(
                dir=edf_dir_1["dir"],
            )
            out_1 = stub.prepareEdfDir(edf_1)
            rep.append(out_1)
        except grpc.RpcError as rpc_error:
            print(f"gRPC Error: {rpc_error}.")
        return rep


def test_grpc():
    dirs = get_grpc()
    assert dirs is not None
    print(f"dirs is {dirs}")
    assert dirs[0].dir == out_dir_1["dir"]
    assert os.path.exists("data/out/cons-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv")
    assert os.path.exists("data/out/cons-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv")
    assert os.path.exists("data/out/res-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv")
    assert os.path.exists("data/out/res-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv")
    assert os.path.exists("data/out/feats-v0_6/dev/01_tcp_ar/002/00009578/00009578_s002_t001.csv")
    assert os.path.exists("data/out/feats-v0_6/dev/01_tcp_ar/002/00009578/00009578_s006_t001.csv")


if __name__ == "__main__":
    print("Executing script:")
    dirs = get_grpc()
    print(dirs)
