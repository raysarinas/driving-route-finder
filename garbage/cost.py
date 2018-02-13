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

        u = e[0]
        v = e[1]
        lon1, lat1 = self.locDict[u]# self.location[u]
        lon2, lat2 = self.locDict[v]
        e_dist = math.sqrt( (lat2 - lat1)**2 + (lon2 - lon1)**2 )
        #e_dist = int(e_dist)
        return e_dist
