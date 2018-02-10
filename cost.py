import math

class CostDistance():
    """
    A class with a method called distance that will return the Euclidean
    between two given vertices.
    """

    def __init__(self, location):
        """
        Creates an instance of the CostDistance class and stores the
        dictionary "location" as a member of this class.
        """

        self.locDict = location

    def distance(self, e):
        """
        Here e is a pair (u,v) of vertices.
        Returns the Euclidean distance between the two vertices u and v.
        """

        u, v = e
        lon1, lat1 = self.locDict[u]# self.location[u]
        lon2, lat2 = self.locDict[v]
        e_dist = math.sqrt( (lat2[0] - lat1[0])**2 + (lon2[1] - lon1[1])**2 )
        return int(e_dist)
