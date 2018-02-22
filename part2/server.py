''' SERVER BEING USED FOR PART 2 💩
    I'll put back the docstring comment description thingamobobs later
'''

from graph import Graph
from binary_heap import BinaryHeap
import math
import sys

# modules for python-arduino communication I guess or whatever
from serial import Serial
from time import sleep

def least_cost_path(graph, start, dest, cost):
    reached = {} # empty dictionary
    events = BinaryHeap() # empty heap
    events.insert((start, start), 0) # vertex s burns at time 0

    while len(events) > 0:
        edge, time = events.popmin()
        if edge[1] not in reached:
            reached[edge[1]] = edge[0] # burn vertex v, record predecessor u
            for nbr in graph.neighbours(edge[1]):
                events.insert((edge[1], nbr), time + cost.distance((edge[1], nbr)))

    # if the dest is not in the reached dictionary, then return an empty list
    if dest not in reached:
      return []

    current = dest
    path = [current]
    while current != start:
        current = reached[current]
        path.append(current)
    path = path[::-1]
    return path


def load_edmonton_graph(filename):
    # get the file and open it
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        # split at each comma and store data appropriately
        for line in filename:
            row = line.strip().split(",")

            # if first character is a 'V' store vertex data, elif 'E' store edge data
            if row[0] == "V":
                graph.add_vertex(int(row[1]))

                # store coordinates in location dictionary
                latitude = int(float(row[2]) * 100000)
                longitude = int(float(row[3]) * 100000)
                location[int(row[1])] = (latitude, longitude)

            elif row[0] == "E":
                graph.add_edge((int(row[1]), int(row[2])))

    return graph, location

class CostDistance():
    def __init__(self, location):
        self.locDict = location

    def distance(self, e):
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]

        # calculate the Euclidean distance between two points(x1,y1) and (x2,y2)
        e_dist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
        return e_dist

def euc_dist(point, coord):
    sum = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
    dist = math.sqrt(sum)

    return dist


def process_input(request, location):
    # store list of input things into appropriate variables
    valid = request[0]
    startcoord = [int(request[1]), int(request[2])]
    destination = [int(request[3]), int(request[4])]

    # initialize minimum start/end and start/end vertex values
    minStart = float('inf')
    minEnd = float('inf')
    startV = None
    endV = None

    # check if a valid request has been inputted
    checkrequest(valid)

    # find the nearest vertex to the start and destination/end points
    # that have been inputted/requested
    for vertex, point in location.items():
        startDist = euc_dist(point, startcoord)
        endDist = euc_dist(point, destination)
        if startDist <= minStart:
            startV = vertex
            minStart = startDist
        if endDist <= minEnd:
            endV = vertex
            minEnd = endDist

    return startV, endV


if __name__ == "__main__":
    with Serial("/dev/ttyACM0", baudrate=9600, timeout=5) as ser:
        while True:
