import math
import time

from app.services.sub_service.frame_cache import FrameCacheService
from app.services.sub_service.speed_smoother import SpeedSmoother

class SpeedEstimationService:

    def __init__(self, pixel_to_meter=0.05):
        self.cache = FrameCacheService()
        self.smoother = SpeedSmoother()
        self.pixel_to_meter = pixel_to_meter

    def _distance(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

    def estimate(self, tracked_objects):

        results = []
        current_ids = set()
        now = time.time()

        for obj in tracked_objects:
            obj_id = obj["id"]
            x1,y1,x2,y2 = obj["bbox"]

            center = ((x1+x2)/2, (y1+y2)/2)
            current_ids.add(obj_id)

            prev = self.cache.get(obj_id)

            if prev is None:
                speed = 0
            else:
                dt = now - prev["time"]

                if dt < 1e-4:
                    speed = 0
                else:
                    pixel_distance = self._distance(prev["center"], center)

                    if pixel_distance < 2:
                        speed = 0
                    else:
                        speed_mps = (pixel_distance * self.pixel_to_meter) / dt
                        speed = speed_mps * 3.6

            speed = self.smoother.smooth(obj_id, speed)

            self.cache.update(obj_id, center)

            obj["speed"] = speed
            results.append(obj)

        self.cache.clear_missing(current_ids)
        self.smoother.clear_missing(current_ids)

        return results