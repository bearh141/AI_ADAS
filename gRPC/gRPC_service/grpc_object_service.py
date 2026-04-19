import time
import cv2
import numpy as np

import proto.object_pb2 as object_pb2
import proto.object_pb2_grpc as object_pb2_grpc

from app.services.object_service import object_prediction
from app.services.sub_service.tracking_service import TrackingService
from app.services.sub_service.speed_service import SpeedEstimationService


class ObjectService(object_pb2_grpc.ObjectServiceServicer):

    def __init__(self):
        self.tracker = TrackingService()
        self.speed_service = SpeedEstimationService()

    def Detect(self, request, context):
        start_time = time.time()

        try:
            # decode image
            np_arr = np.frombuffer(request.image, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                return object_pb2.DetectResponse()

            # 1. detection
            detections = object_prediction(frame)

            # 2. tracking
            tracks = self.tracker.track(detections)

            # 3. speed
            results = self.speed_service.estimate(tracks)

            objects = []
            for obj in results:
                objects.append(
                    object_pb2.ObjectData(
                        id=obj["id"],
                        label=obj.get("label", ""),
                        confidence=obj.get("confidence", 0),
                        bbox=obj["bbox"],
                        speed=obj["speed"]
                    )
                )

            return object_pb2.DetectResponse(
                objects=objects,
                processing_time=time.time() - start_time
            )

        except Exception as e:
            print("Object gRPC Error:", e)
            return object_pb2.DetectResponse()