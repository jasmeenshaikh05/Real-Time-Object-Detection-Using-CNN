class Analytics:

    def __init__(self, min_frames=5, ttl=30):

        self.min_frames = min_frames
        self.ttl = ttl

        # person tracking stabilization
        self.tracks = {}

        # counts for other classes
        self.other_counts = {}


    def update(self, detections):

        current_ids = set()
        self.other_counts = {}

        for det in detections:

            label = det["class"]

            # PERSON → tracked counting
            if label == "person":

                tid = det["id"]
                current_ids.add(tid)

                if tid not in self.tracks:
                    self.tracks[tid] = {
                        "frames_seen": 1,
                        "missing": 0,
                        "counted": False
                    }
                else:
                    self.tracks[tid]["frames_seen"] += 1
                    self.tracks[tid]["missing"] = 0

            # OTHER OBJECTS → simple counting
            else:

                if label not in self.other_counts:
                    self.other_counts[label] = 0

                self.other_counts[label] += 1


        # handle disappeared persons
        for tid in list(self.tracks.keys()):

            if tid not in current_ids:

                self.tracks[tid]["missing"] += 1

                if self.tracks[tid]["missing"] > self.ttl:
                    del self.tracks[tid]


        # mark stable tracks
        for tid, info in self.tracks.items():

            if info["frames_seen"] >= self.min_frames:
                info["counted"] = True


    def get_counts(self):

        person_count = sum(
            1 for info in self.tracks.values() if info["counted"]
        )

        counts = {"person": person_count}

        # add other object counts
        for k, v in self.other_counts.items():
            counts[k] = v

        return counts