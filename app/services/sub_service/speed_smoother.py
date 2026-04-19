class SpeedSmoother:
    def __init__(self, alpha=0.6):
        self.alpha = alpha
        self.history = {}

    def smooth(self, obj_id, speed):
        if obj_id not in self.history:
            self.history[obj_id] = speed
            return speed

        prev = self.history[obj_id]
        smoothed = self.alpha * speed + (1 - self.alpha) * prev

        self.history[obj_id] = smoothed
        return smoothed

    def clear_missing(self, current_ids):
        self.history = {
            k: v for k, v in self.history.items()
            if k in current_ids
        }