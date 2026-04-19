import grpc
from concurrent import futures

from app.config.settings import settings
import proto.sign_pb2_grpc as sign_pb2_grpc
import proto.object_pb2_grpc as object_pb2_grpc
import proto.lane_pb2_grpc as lane_pb2_grpc

from gRPC.gRPC_service.grpc_object_service import ObjectService
from gRPC.gRPC_service.grpc_sign_service import SignService
from gRPC.gRPC_service.grpc_lane_service import LaneService


def start_grpc_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4)
    )

    #SignService
    sign_pb2_grpc.add_SignServiceServicer_to_server(
        SignService(), server
    )

    #ObjectService
    object_pb2_grpc.add_ObjectServiceServicer_to_server(
        ObjectService(), server
    )

    #LaneService
    lane_pb2_grpc.add_LaneServiceServicer_to_server(
        LaneService(), server
    )

    server.add_insecure_port(settings.GRPC_PORT)

    server.start()

    print("🚀 gRPC server running on port " + settings.GRPC_PORT)

    return server