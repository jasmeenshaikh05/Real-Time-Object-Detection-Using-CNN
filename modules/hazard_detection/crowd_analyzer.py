class CrowdAnalyzer:

    def __init__(self):

        pass


    def analyze(self, detections):

        person_count = 0

        for det in detections:

            if det["class"] == "person":

                person_count += 1


        density = "LOW"

        if person_count > 5:
            density = "MEDIUM"

        if person_count > 10:
            density = "HIGH"


        stampede_risk = False

        if person_count > 15:
            stampede_risk = True


        return {

            "count": person_count,
            "density": density,
            "risk": stampede_risk

        }