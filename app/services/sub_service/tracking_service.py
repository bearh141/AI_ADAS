import math

class TrackingService:
    def __init__(self):
        self.prev_objects = {}
        self.next_id = 1

    def _distance(self, c1, c2):
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

    def track(self, detections):
        results = []
        new_objects = {}

        for det in detections:
            x1,y1,x2,y2 = det["bbox"]
            center = ((x1+x2)/2, (y1+y2)/2)

            matched_id = None

            for obj_id, prev_center in self.prev_objects.items():
                if self._distance(center, prev_center) < 50:
                    matched_id = obj_id
                    break

            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

            new_objects[matched_id] = center

            det["id"] = matched_id
            results.append(det)

        self.prev_objects = new_objects

        return results