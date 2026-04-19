import cv2
import numpy as np

import proto.sign_pb2 as sign_pb2
import proto.sign_pb2_grpc as sign_pb2_grpc

from app.services.sign_service import sign_prediction


class SignService(sign_pb2_grpc.SignServiceServicer):

    def Predict(self, request, context):
        image_bytes = request.image

        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = sign_prediction(frame)

        detections = []
        meta = None

        for r in results:
            if "meta" in r:
                meta = r["meta"]
                continue

            detections.append(
                sign_pb2.Detection(
                    box=r["box"],
                    confidence=r["confidence"],
                    class_id=r["class_id"],
                    class_name=r["class_name"]
                )
            )

        return sign_pb2.SignResponse(
            detections=detections,
            meta=sign_pb2.Meta(
                start_time=meta["start_time"],
                end_time=meta["end_time"],
                duration_ms=meta["duration_ms"]
            ) if meta else None
        )