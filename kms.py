from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
import math

def least_cost_path(graph, start, dest, cost):
    reached = {} # empty dictionary
    events = BinaryHeap() # empty heap
    events.insert((start, start), 0) # vertex s burns at time 0

    while len(events) > 0:
        print("Loop 1")
        vertices, time = events.popmin()
        print(type(vertices))
        print(type(vertices[0]))
        if vertices[1] not in reached:
            reached[vertices[1]] = vertices[0]# vertices[0] = reached[vertices[1]]   burn vertex v, record predecessor u
            for n in graph.neighbours(vertices[1]):
                 # new event: edge (v,w) started burning
                print("Loop 2")
                events.insert(([vertices[1]], n), time + cost.distance((vertices[1], n)))

            if vertices[1] == dest:
                break

    #return reached
    print("Done")
    #find path to see if a path exists
    # return empty list if dest cannot be reached/if no path from start to dest exists
    if dest not in reached:
      return []

    # if the destination gets reached we can form a minimum path

    current = dest
    path = [current]

    while current != start:
        # print("Loop 3")
        print(dest)
        print(type(dest))
        current = reached[current]
        #current = reached[current]
        path.append(current)

    #or while reached[current] != start:
    #path.append(reached[current])
    #    current = reached[current]

    path = path[::-1]
    return path

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

import math

class CostDistance():
    def __init__(self, location):
        self.locDict = location

    def distance(self, e):
        lon1, lat1 = self.locDict[e[0]]# self.location[u]
        lon2, lat2 = self.locDict[e[1]]
        e_dist = math.sqrt( (lat2 - lat1)**2 + (lon2 - lon1)**2 )
        #e_dist = int(e_dist)
        return e_dist

''' ------------------------------------ '''
''' ------------------------------------ '''

#yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
# location is a dict where keys are the vertices and holds a tuple of the coordinates
print("start")
yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
cost = CostDistance(location)
reached = least_cost_path(yegGraph, 30198538, 30198540, cost)
print(reached)
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
