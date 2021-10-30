
import grpc
import aura_dataprep_pb2 as pb2
import aura_dataprep_pb2_grpc as pb2_grpc
import time
import pytest
from typing import List, Any


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


def get_grpc() -> List[Any]:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = pb2_grpc.AuraDataprepStub(channel)
        rep: List[Any] = []
        try:
            edf_1 = pb2.EdfFile(edf = edf_file_1["edf"],
                                anno = edf_file_1["anno"],
            )
            out_1 = stub.prepareEdfFile(edf_1)
            print(f"- edf {out_1}.")
            #print(f"  anno {out_1.anno}.")
            #print(f"  feats {out_1.anno}.")
            rep.append(out_1)
            time.sleep(1)
            # out_2 = stub.prepareEdfFile(pb2.EdfFile(edf_file_2))
            # print(f"- edf {out_1.edf}.")
            # print(f"  anno {out_1.anno}.")
            # print(f"  feats {out_1.anno}.")
            # rep.append(out)
        except grpc.RpcError as rpc_error:
            print(f"gRPC Error: {rpc_error}.")
        return rep

def test_grpc():
    files = get_grpc()
    assert files is not None
    assert files[0].edf == edf_file_1["edf"]
    assert files[0].anno == edf_file_1["anno"]
    assert files[0].feats == edf_file_1["feats"]
    
if __name__ == "__main__":
   files = get_grpc()
   print("Executing script:")
   print(files)
