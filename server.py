# main program here apparently

from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
from dijkstra import least_cost_path
from build import load_edmonton_graph
from cost import CostDistance

#yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
# location is a dict where keys are the vertices and holds a tuple of the coordinates

if __name__ == "__main__":
    # Code for processing route finding requests here
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
    cost = CostDistance(location)

    request = input().strip().split(" ")
    vertices = list(yegGraph.get_vertices())
    request[1] = int(request[1])
    request[2] = int(request[2])
    request[3] = int(request[3])
    request[4] = int(request[4])

    test1 = [int(request[1]), int(request[2])]
    test2 = [int(request[3]), int(request[4])]
    start = None
    end = None

    if request[0] == 'R':
        for identity, coord in location.items():
            if coord[0] == test1[0] and coord[1] == test2[1]:
                start = identity #int(identity)
            elif coord[0] == test2[0] and coord[1] == test2[1]:
                end = identity #int(identity)

        reached = least_cost_path(yegGraph, start, end, cost)
        print('N', len(reached))
        for something in range(len(reached)):
            response = input()
            if response == 'A':
                print('W', reached[something])
            else:
                print("Invalid response")
                something -= 1
        print('E')
    else:
        print('invalid request')
