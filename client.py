import grpc
import xscad_pb2
import xscad_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = xscad_pb2_grpc.XSCADServiceStub(channel)

        actions = [
            xscad_pb2.Action(name="action1", parameters={"param1": "value1"}),
            #xscad_pb2.Action(name="invalid_action", parameters={"paramA": "valueA"})  # 不合法的動作
        ]

        try:
            response = stub.ExecuteAction(
                xscad_pb2.ActionRequest(
                    header=xscad_pb2.Header(
                        token="my_token",
                        account="my_account",
                        bob="bob_value",
                        alice="alice_value"
                    ),
                    body=xscad_pb2.Body(
                        actions=actions,
                        timestamp=1234567890
                    )
                )
            )
            print("Client received:", response.result)
        except grpc.RpcError as e:
            print(f"Error: {e.code()}: {e.details()}")

if __name__ == '__main__':
    run()
