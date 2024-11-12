from concurrent import futures
import grpc
import xscad_pb2
import xscad_pb2_grpc

class XSCADService(xscad_pb2_grpc.XSCADServiceServicer):
    def __init__(self):
        self.valid_actions = {"action1", "action2", "action3"}

    def ExecuteAction(self, request, context):
        actions_result = []
        for action in request.body.actions:
            if action.name not in self.valid_actions:
                context.set_details(f"Invalid action: {action.name}")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return xscad_pb2.ActionResponse(result="", success=False)

            action_details = f"Action '{action.name}' with parameters {dict(action.parameters)} executed."
            actions_result.append(action_details)

        result = "; ".join(actions_result)
        return xscad_pb2.ActionResponse(result=result, success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xscad_pb2_grpc.add_XSCADServiceServicer_to_server(XSCADService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
