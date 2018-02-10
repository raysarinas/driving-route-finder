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
print(waypoints)


    # response = input()
    # if response == 'A':
    #     print('W', )



# shortest_path = least_cost_path(yegGraph, )
#
# yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
# cost = CostDistance(location)
# reached = least_cost_path(yegGraph, start, end, cost)
# print(reached)
'''
request = input().strip().split(" ")
valid = request[0]
coord1 = [int(request[1]), int(request[2])]
coord2 = [int(request[3]), int(request[4])]
start = None
end = None

if valid == 'R':
    for vertices, point in location.items():
        if point[0] == coord1[0] and point[1] == coord1[1]:
            start = vertices
        if point[0] == coord2[0] and point[1] == coord2[1]:
            end = vertices

path = least_cost_path(yegGraph, start, end, cost)
pathlen = len(path)
print('N', pathlen)
for i in range(pathlen):
    response = input()
    if response == 'A':
        print('W', path)
    print('E')
'''
        # reached_paths = least_cost_path(edmonton_Graph, startpoint, endpoint, costObject)
        # print('N',len(reached_paths))
        # for returns in range(len(reached_paths)):
        #     returnmsg= input()
        #     if returnmsg =='A':
        #         print('W',reached_paths[returns])
        # print('E')

# if __name__ == "__main__":
#     # Code for processing route finding requests here
#
#
#     request = input().strip().split(" ")
#     vertices = list(yegGraph.get_vertices())
#     request[1] = int(request[1])
#     request[2] = int(request[2])
#     request[3] = int(request[3])
#     request[4] = int(request[4])
#
#     test1 = [int(request[1]), int(request[2])]
#     test2 = [int(request[3]), int(request[4])]
#     start = None
#     end = None
#     if request[0] == 'R':
#         for identity, coord in location.items():
#             if coord[0] == test1[0] and coord[1] == test1[1]:
#                 start = identity #int(identity)
#             elif coord[0] == test2[0] and coord[1] == test2[1]:
#                 end = identity #int(identity)
#
#         reached = least_cost_path(yegGraph, 30198538, 30198540, cost)
#         print('N', len(reached))
#         for something in range(len(reached)):
#             response = input()
#             if response == 'A':
#                 print('W', reached)
#             else:
#                 print("Invalid response")
#                 something -= 1
#         print('E')
#     else:
#         print('invalid request')
