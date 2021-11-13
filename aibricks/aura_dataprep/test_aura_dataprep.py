import grpc
import aura_dataprep_pb2 as pb2
import aura_dataprep_pb2_grpc as pb2_grpc
import time
from typing import List, Any
import os

grpc_url = "localhost:8061"

edf_dir_1 = {
    "dir": "data/tuh/dev/01_tcp_ar/002/00009578/",
}

out_dir_1 = {
    "dir": "out/tuh/dev/01_tcp_ar/002/00009578/",
}


def _set_path(path):
    # Prepare variables with absolute paths
    cwd = os.getcwd()
    print(f"PATH {cwd}")
    return cwd + "/" + path


def get_grpc() -> List[Any]:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = pb2_grpc.AuraDataprepStub(channel)
        rep: List[Any] = []
        try:
            edf_1 = pb2.EdfDir(
                dir=_set_path(edf_dir_1["edf"]),
            )
            out_1 = stub.prepareEdfDir(edf_1)
            print(f"- out_1 {out_1}.")
            rep.append(out_1)
            time.sleep(1)
            edf_2 = pb2.EdfDir(
                edf=_set_path(edf_dir_2["edf"]),
                anno=_set_path(edf_dir_2["anno"]),
            )
            out_2 = stub.prepareEdfDir(edf_2)
            print(f"- out_2 {out_2}.")
            rep.append(out_2)
        except grpc.RpcError as rpc_error:
            print(f"gRPC Error: {rpc_error}.")
        return rep


def test_grpc():
    dirs = get_grpc()
    assert dirs is not None
    assert dirs[0].dir == _set_path(out_dir_1["dir"])


if __name__ == "__main__":
    print("Executing script:")
    dirs = get_grpc()
    print(dirs)
