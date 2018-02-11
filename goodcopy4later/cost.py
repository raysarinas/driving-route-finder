import math

class CostDistance():
    def __init__(self, location):
        self.locDict = location

    def distance(self, e):
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]
        e_dist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
        return e_dist
