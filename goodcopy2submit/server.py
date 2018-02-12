from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
import math
from dijkstra import least_cost_path
from build import load_edmonton_graph
from cost import CostDistance

def checkinput():
    ''' checks if there is correct response from user to print out the next
        waypoint for the least cost path. won't skip over a waypoint because
        if input is incorrect will recursively wait until there is correct
        response i guess. returns none and takes no parameters/arguments '''

    response = input()
    if response == 'A':
        print('W', lat, lon)
    else:
        print('try again')
        checkinput()

def euc_dist(point, coord):
    sum = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
    dist = math.sqrt(sum)

    return dist


if __name__ == "__main__":
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
        print("try again xoxo - gossip girl")

    reached = least_cost_path(yegGraph, start, end, cost)
    waypoints = len(reached)

    print('N', waypoints)

    for path in reached:
        (lat, lon) = location[path]
        checkinput()

    print('E')
