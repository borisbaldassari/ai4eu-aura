
import grpc
import edf_databroker_train_pb2 as pb2
import edf_databroker_train_pb2_grpc as pb2_grpc
import time
import pytest
from typing import List, Any


grpc_url = "localhost:8061"

edf_file_1 = {
    "edf": "data/01_tcp_ar/002/00009578/00009578_s006_t001.edf",
    "anno": "data/01_tcp_ar/002/00009578/00009578_s006_t001.tse_bi"
}

edf_file_2 = {
    "edf": "data/01_tcp_ar/002/00009578/00009578_s002_t001.edf",
    "anno": "data/01_tcp_ar/002/00009578/00009578_s002_t001.tse_bi" 
}


def get_grpc() -> List[Any]:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = pb2_grpc.EdfDatabrokerStub(channel)
        rep: List[Any] = []
        empty = pb2.Empty()
        while True:
            try:
                file = stub.get_next_edf_file(empty)
                rep.append(file)
                print(f"- edf {file.edf}.")
                print(f"  anno {file.anno}.")
                time.sleep(1)
            except grpc.RpcError as rpc_error:
                if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                    break
        return rep

def test_grpc():
    files = get_grpc()
    assert files is not None
    assert files[0].edf == edf_file_1["edf"]
    assert files[0].anno == edf_file_1["anno"]
    assert files[1].edf == edf_file_2["edf"]
    assert files[1].anno == edf_file_2["anno"]

if __name__ == "__main__":
   files = get_grpc()
   print("Executing script:")
   print(files)
