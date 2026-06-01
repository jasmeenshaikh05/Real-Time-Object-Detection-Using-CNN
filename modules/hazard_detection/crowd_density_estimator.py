class CrowdDensityEstimator:

    def __init__(self):

        print("Crowd density estimator ready")

        self.low_threshold = 10
        self.medium_threshold = 30
        self.high_threshold = 60


    def estimate(self, detections):

        person_count = 0

        for det in detections:

            # some detections come as dict with 'class'
            if "class" in det:

                if det["class"] == "person":
                    person_count += 1

            # some trackers return 'cls'
            elif "cls" in det:

                if det["cls"] == "person":
                    person_count += 1


        if person_count < self.low_threshold:
            level = "LOW"

        elif person_count < self.medium_threshold:
            level = "MEDIUM"

        elif person_count < self.high_threshold:
            level = "HIGH"

        else:
            level = "EXTREME"


        return {
            "count": person_count,
            "level": level
        }