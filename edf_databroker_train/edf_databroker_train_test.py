
import grpc
import edf_databroker_train_pb2 as pb2
import edf_databroker_train_pb2_grpc as pb2_grpc
import time

grpc_url = "localhost:8061"
    
with grpc.insecure_channel(grpc_url) as channel:
    stub = pb2_grpc.EdfDatabrokerStub(channel)

    empty = pb2.Empty()
    while True:
        try:
            file = stub.get_next_edf_file(empty)
            print(f"- edf {file.edf}.")
            print(f"  anno {file.anno}.")
            time.sleep(1)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                break

