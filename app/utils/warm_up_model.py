from proto import object_pb2, lane_pb2, sign_pb2


def warmup_all():
    import numpy as np
    import cv2

    print("🔥 Starting full system warm-up...")

    from gRPC.gRPC_service.grpc_object_service import ObjectService
    from gRPC.gRPC_service.grpc_lane_service import LaneService
    from gRPC.gRPC_service.grpc_sign_service import SignService

    obj_service = ObjectService()
    lane_service = LaneService()
    sign_service = SignService()

    dummy = np.zeros((640, 640, 3), dtype=np.uint8)
    _, buffer = cv2.imencode('.jpg', dummy)
    img_bytes = buffer.tobytes()

    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    print("  → Warming up ObjectService...")
    obj_service.Detect(
        object_pb2.DetectRequest(image=img_bytes),
        None
    )

    print("  → Warming up LaneService...")
    lane_service.Predict(
        lane_pb2.LaneRequest(image=img_bytes),
        None
    )

    print("  → Warming up SignService...")
    sign_service.Predict(
        sign_pb2.SignRequest(image=img_bytes),
        None
    )

    print("✅ Warm-up completed!")
