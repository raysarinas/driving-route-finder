# main program here apparently

from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
from dijkstra import least_cost_path
from build import load_edmonton_graph
from cost import CostDistance

yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
# location is a dict where keys are the vertices and holds a tuple of the coordinates





if __name__ == "__main__":
    # Code for processing route finding requests here
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')

    request = input().strip().split(" ")
    valid = False
    vertices = yegGraph.get_vertices()
    print(vertices)

    if request[0] == 'R':
        valid = True
    else:
        print('invalid request')
