import math
from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
from dijkstra import least_cost_path
from build import load_edmonton_graph
from cost import CostDistance

def checkinput():
    """
    Checks user input for response to print out the next waypoint coordinates.
    Will not skip over a waypoint because if the input is invalid, function
    will recursively call itself until there is a correct response.
    """

    response = input()
    if response == 'A':
        print('W', lat, lon)
    else:
        print('try again')
        checkinput()

def euc_dist(point, coord):
    """
    Here point and coord are tuples that contain coordinates
    Returns Euclidean distance between a point and coordinate.
    """

    sum = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
    dist = math.sqrt(sum)

    return dist


if __name__ == "__main__":
    """ everything below is done according to assignment description """
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
    cost = CostDistance(location)
    request = input().strip().split(" ")
    valid = request[0]
    startcoord = [int(request[1]), int(request[2])]
    destination = [int(request[3]), int(request[4])]
    minStart = float('inf')
    minEnd = float('inf')
    startV = None
    endV = None

    for vertex, point in location.items():
        startDist = euc_dist(point, startcoord)
        endDist = euc_dist(point, destination)
        if startDist <= minStart:
            startV = vertex
            minStart = startDist
        if endDist <= minEnd:
            endV = vertex
            minEnd = endDist

    start = startV
    end = endV

    if start == None or end == None:
        print("u should never have gotten to this point")
        print("try again xoxo")
        print("               - gossip girl ;*")

    reached = least_cost_path(yegGraph, start, end, cost)
    waypoints = len(reached)

    print('N', waypoints)

    if len(reached) == 0:
        print("no path, please try again and restart program")

    for path in reached:
        (lat, lon) = location[path]
        checkinput()

    print('E')
