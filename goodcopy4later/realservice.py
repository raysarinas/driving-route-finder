from graph import Graph
from binary_heap import BinaryHeap
import math


def checkinput():
    '''
        Check if the user has sent an A and will then print out the next waypoint
        Prevents missing a waypoint because if they don't input A, the method
        will recursively call and will get the user's input again '''

    ack = input().strip()
    if ack == 'A':
        print('W', latitude, longitude)
    else:
        checkinput()


def findmin(s, end, loc):
    minStart = 1000000
    minEnd = 1000000
    minStartVert = None
    minEndVert = None

    for vert, tup in loc.items():
        if (abs(tup[0] - s[0]) + abs(tup[1] - s[1])) <= minStart:
            minStartVert = vert
            minStart = abs(tup[0] - s[0]) + abs(tup[1] - s[1])
        if (abs(tup[0] - end[0]) + abs(tup[1] - end[1])) <= minEnd:
            minEndVert = vert
            minEnd = abs(tup[0] - end[0]) + abs(tup[1] - end[1])

    return minStartVert, minEndVert


def least_cost_path(graph, start, dest, cost):
    reached = {}  # empty dictionary
    events = BinaryHeap()  # empty heap
    events.insert((start, start), 0)  # vertex s burns at time 0

    while len(events) > 0:
        edge, time = events.popmin()
        if edge[1] not in reached:
            reached[edge[1]] = edge[0]
            for nbr in graph.neighbours(edge[1]):
                events.insert((edge[1], nbr), time + cost.distance((edge[1], nbr)))
    # if the dest is not in reached, then no route was found
    if dest not in reached:
        return []

    current = dest
    route = [current]
    # go through the reached vertices until we get back to start and append
    # each vertice that we "stop" at
    while current != start:
        current = reached[current]
        route.append(current)
    # reverse the list because we made a list that went from the dest to start
    route = route[::-1]
    return route


class CostDistance():
    def __init__(self, location):
        self.locDict = location

    def distance(self, e):
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]
        edist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
        return edist


def load_edmonton_graph(filename):
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        for line in filename:
            lines = line.strip().split(",")

            if lines[0] == "V":
                graph.add_vertex(int(lines[1]))
                latitude = int(float(lines[2]) * 100000)
                longitude = int(float(lines[3]) * 100000)
                location[int(lines[1])] = (latitude, longitude)

            elif lines[0] == "E":
                graph.add_edge((int(lines[1]), int(lines[2])))

    return graph, location


if __name__ == "__main__":
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
    cost = CostDistance(location)
    selectPoints = input().strip().split(" ")
    valid = selectPoints[0]
    startcoord = [int(selectPoints[1]), int(selectPoints[2])]
    destination = [int(selectPoints[3]), int(selectPoints[4])]
    start = None
    end = None

    start, end = findmin(startcoord, destination, location)

    # for vertex, point in location.items():
    #     if point[0] == startcoord[0] and point[1] == startcoord[1]:
    #         start = vertex
    #     if point[0] == destination[0] and point[1] == destination[1]:
    #         end = vertex

    if start is None or end is None:
        print("Error")

    reached = least_cost_path(yegGraph, start, end, cost)
    print('N', len(reached))

    for route in reached:
        (latitude, longitude) = location[route]
        checkinput()

    print('E')
