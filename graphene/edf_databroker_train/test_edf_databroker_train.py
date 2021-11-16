import google
import grpc
import edf_databroker_train_pb2 as pb2
import edf_databroker_train_pb2_grpc as pb2_grpc
import time
import pytest
from typing import List, Any


grpc_url = "localhost:8061"

edf_dir_1 = {
    "dir": "01_tcp_ar/002/00009578",
}


def get_grpc() -> List[Any]:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = pb2_grpc.EdfDatabrokerStub(channel)
        rep: List[Any] = []
        empty = pb2.Empty()
        while True:
            try:
                edf_dir = stub.get_next_edf_dir(empty)
                rep.append(edf_dir)
                print(f"  dir {edf_dir.dir}.")
                time.sleep(1)
            except grpc.RpcError as rpc_error:
                if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                    print(f"grpc reported not found")
                    break
        return rep


def test_grpc():
    dirs = get_grpc()
    assert dirs is not None
    print(f"dirs is {dirs}")
    assert dirs[0].dir == edf_dir_1["dir"]


if __name__ == "__main__":
    print("Executing script:")
    dirs = get_grpc()
    print("Executing script:")
    print(dirs)
