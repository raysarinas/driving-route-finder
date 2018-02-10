from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
import math

def least_cost_path(graph, start, dest, cost):
    reached = {} # empty dictionary
    events = BinaryHeap() # empty heap
    events.insert((start, start), 0) # vertex s burns at time 0

    while len(events) > 0:
        edge, time = events.popmin()
        if edge[1] not in reached:
            reached[edge[1]] = edge[0]
            for nbr in graph.neighbours(edge[1]):
                events.insert((edge[1], nbr), time + cost.distance((edge[1], nbr)))
    return reached

''' ------------------------------------ '''
''' ------------------------------------ '''

def load_edmonton_graph(filename):
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        for line in filename:
            row = line.strip().split(",")

            if row[0] == "V":
                graph.add_vertex(int(row[1]))
                latitude = int(float(row[2]) * 100000)
                longitude = int(float(row[3]) * 100000)
                location[int(row[1])] = (latitude, longitude)

            elif row[0] == "E":
                graph.add_edge((int(row[1]), int(row[2])))

    return graph, location

''' ------------------------------------ '''
''' ------------------------------------ '''

class CostDistance():
    def __init__(self, location):
        self.locDict = location

    def distance(self, e):
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]
        e_dist = math.sqrt( (lat2 - lat1) ** 2 + (lon2 - lon1) ** 2 )
        return e_dist

''' ------------------------------------ '''
''' ------------------------------------ '''

def checkinput():
    response = input()
    if response == 'A':
        print('W', lat, lon)
    else:
        print('try again dumbass')
        checkinput()

''' ------------------------------------ '''
''' ------------------------------------ '''

yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
cost = CostDistance(location)
request = input().strip().split(" ")
valid = request[0]
startcoord = [int(request[1]), int(request[2])]
destination = [int(request[3]), int(request[4])]
print(startcoord, destination)
start = None
end = None

for vertex, point in location.items():
    if point[0] == startcoord[0] and point[1] == startcoord[1]:
        start = vertex
    if point[0] == destination[0] and point[1] == destination[1]:
        end = vertex

if start == None or end == None:
    print("god is dead")
else:
    print(start, end)

reached = least_cost_path(yegGraph, start, end, cost)
''' LEAST COST PATH KEEPS RETURNING 57779 IDK WHY '''
waypoints = len(reached)
print(reached)
print('N', waypoints)

for path in reached:
    (lat, lon) = location[path]
    checkinput()

print('E')
