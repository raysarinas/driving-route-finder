# main program here apparently

from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
from dijkstra import least_cost_path
from build import load_edmonton_graph
from cost import CostDistance

request = input().strip().split(" ")
print(request)
valid = False

if request[0] == 'R':
    valid = True
else:
    print('invalid request')


#def nearest_vertex():

#def output():

#def communicate():

if __name__ == "__main__":
    # Code for processing route finding requests here
    yegGraph = load_edmonton_graph('edmonton-roads-2.0.1.txt')
