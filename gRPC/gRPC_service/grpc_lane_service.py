import time
import cv2
import numpy as np

import proto.lane_pb2 as lane_pb2
import proto.lane_pb2_grpc as lane_pb2_grpc

from app.services.lane_service import lane_prediction


class LaneService(lane_pb2_grpc.LaneServiceServicer):

    def Predict(self, request, context):
        start_time = time.time()

        try:
            # decode image
            np_arr = np.frombuffer(request.image, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                return lane_pb2.LaneResponse()

            # prediction
            detections = lane_prediction(frame)

            results = []

            for det in detections:
                # 🔥 FIX format giống proto
                box = det.get("box", [])

                results.append(
                    lane_pb2.LaneData(
                        box=box,
                        confidence=det.get("confidence", 0),
                        class_id=det.get("class_id", 0),
                        class_name=det.get("class_name", "")
                    )
                )

            return lane_pb2.LaneResponse(
                detections=results,
                meta=lane_pb2.LaneMeta(
                    processing_time=time.time() - start_time
                )
            )

        except Exception as e:
            print("Lane gRPC Error:", e)
            return lane_pb2.LaneResponse()