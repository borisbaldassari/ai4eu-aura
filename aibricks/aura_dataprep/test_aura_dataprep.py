import grpc
import aura_dataprep_pb2 as pb2
import aura_dataprep_pb2_grpc as pb2_grpc
import time
from typing import List, Any
import os

grpc_url = "localhost:8061"

edf_file_1 = {
    "edf": "data/01_tcp_ar/002/00009578/00009578_s006_t001.edf",
    "anno": "data/01_tcp_ar/002/00009578/00009578_s006_t001.tse_bi",
}

edf_file_2 = {
    "edf": "data/01_tcp_ar/002/00009578/00009578_s002_t001.edf",
    "anno": "data/01_tcp_ar/002/00009578/00009578_s002_t001.tse_bi",
}

out_file_1 = {
    "ecg": "out/01_tcp_ar/002/00009578/ecg_00009578_s006_t001.json",
    "anno": "out/01_tcp_ar/002/00009578/annot_00009578_s006_t001.json",
    "feats": "out/01_tcp_ar/002/00009578/feats_00009578_s006_t001.json",
}

out_file_2 = {
    "ecg": "out/01_tcp_ar/002/00009578/ecg_00009578_s002_t001.json",
    "anno": "out/01_tcp_ar/002/00009578/annot_00009578_s002_t001.json",
    "feats": "out/01_tcp_ar/002/00009578/feats_00009578_s002_t001.json",
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
            edf_1 = pb2.EdfFile(
                edf=_set_path(edf_file_1["edf"]),
                anno=_set_path(edf_file_1["anno"]),
            )
            out_1 = stub.prepareEdfFile(edf_1)
            print(f"- out_1 {out_1}.")
            rep.append(out_1)
            time.sleep(1)
            edf_2 = pb2.EdfFile(
                edf=_set_path(edf_file_2["edf"]),
                anno=_set_path(edf_file_2["anno"]),
            )
            out_2 = stub.prepareEdfFile(edf_2)
            print(f"- out_2 {out_2}.")
            rep.append(out_2)
        except grpc.RpcError as rpc_error:
            print(f"gRPC Error: {rpc_error}.")
        return rep


def test_grpc():
    files = get_grpc()
    assert files is not None
    assert files[0].ecg == _set_path(out_file_1["ecg"])
    assert files[0].anno == _set_path(out_file_1["anno"])
    assert files[0].feats == _set_path(out_file_1["feats"])
    assert files[1].ecg == _set_path(out_file_2["ecg"])
    assert files[1].anno == _set_path(out_file_2["anno"])
    assert files[1].feats == _set_path(out_file_2["feats"])


if __name__ == "__main__":
    files = get_grpc()
    print("Executing script:")
    print(files)
