class Tracker:

    def update(self, results):

        detections = []

        for r in results:

            boxes = r.boxes

            if boxes is None:
                continue

            for box in boxes:

                if box.id is None:
                    continue

                track_id = int(box.id.item())
                cls = int(box.cls.item())
                conf = float(box.conf.item())

                detections.append({
                    "id": track_id,
                    "class": r.names[cls],
                    "confidence": conf
                })

        return detections