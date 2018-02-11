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
        print('try again dumbass')
        checkinput()

if __name__ == "__main__":
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
    cost = CostDistance(location)
    request = input().strip().split(" ")
    valid = request[0]
    startcoord = [int(request[1]), int(request[2])]
    destination = [int(request[3]), int(request[4])]
    start = None
    end = None

    for vertex, point in location.items():
        if point[0] == startcoord[0] and point[1] == startcoord[1]:
            start = vertex
        if point[0] == destination[0] and point[1] == destination[1]:
            end = vertex

    if start == None or end == None:
        print("god is dead")
        print("also can't find whatever input that was inputted probably")
    # else:
    #     print(start, end)

    reached = least_cost_path(yegGraph, start, end, cost)
    ''' SOMEONE FIX THIS PLEASE THANKS '''
    ''' LEAST COST PATH KEEPS RETURNING 57779 IDK WHY '''
    ''' DO WE NEED TO FIND THE CLOSEST VERTEX? IM CONFUSED LIKE IDK WHATS HAPPENING '''
    waypoints = len(reached)
    print(reached)
    print('N', waypoints)

    for path in reached:
        (lat, lon) = location[path]
        checkinput()

    print('E')
