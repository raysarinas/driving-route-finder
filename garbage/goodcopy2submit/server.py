import math
import sys
from graph import Graph
from binary_heap import BinaryHeap
from breadth_first_search import breadth_first_search
from dijkstra import least_cost_path
from build import load_edmonton_graph
from cost import CostDistance

def checkrequest(validrequest):
    """
    Check if request character is valid i.e. is equal to the character 'R'.
    If the request is not valid not, exit the program.

    validrequest: first character that is taken from the user input.

    Doesn't return anything.
    """
    if validrequest != 'R':
        print("try again pls input something else thanks bye")
        sys.exit()


def euc_dist(point, coord):
    """
    Here point and coord are tuples that contain coordinates.
    Returns Euclidean distance between a point and coordinate.
    """

    sum = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
    dist = math.sqrt(sum)

    return dist


def process_input(request, location):
    """
    Process the user input. First take the input which has been converted
    into a list and then store it's contents into the appropriate variables.
    Then initiate the minStart and minEnd values as infinity and start and
    destination vertices as None. Then check if the request is valid, and
    then find the nearest vertex to the start and destination/end points
    requested.

    request: list of input contents holding initiating request character,
      and start and destination coordinates.
    location: a dictionary mapping the identifier of a vertex to
      the pair (lat, lon) of geographic coordinates for that vertex.
      These should be integers measuring the lat/lon in 100000-ths
      of a degree.

    Returns the (nearest) start and end vertices of the request.
    """

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


def checkinput():
    """
    Checks user input for response to print out the next waypoint coordinates.
    Will not skip over a waypoint because if the input is invalid, function
    will recursively call itself until there is a correct response.
    Returns nothing.
    """

    response = input() # get input/response
    if response == 'A':
        # if valid response/input, print waypoint with coordinates
        print('W', lat, lon)
    else:  # otherwise recursively wait until 'A' is inputted
        print('try again')
        checkinput()


if __name__ == "__main__":
    # load the graph and get cost object
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
    cost = CostDistance(location)

    # get the input and then call process_input to process the input
    # and get the start and end vertices/coordinates
    # ASSUMES THERE IS ENOUGH INPUT TO SPLIT AND STORE IN A LIST
    # if there is incorrect input then the program ends/exits
    request = input().strip().split(" ")

    if len(request) != 5:
        print("nope wrong input bye")
        sys.exit()

    start, end = process_input(request, location)

    # okay no one should ever reach this point so yeah
    if start == None or end == None:
        print("u should never have gotten to this point")
        print("try again xoxo")
        print(" - gossip girl ;*")

    # find the shortest path via dijkstra's algorithm and get its length/size
    reached = least_cost_path(yegGraph, start, end, cost)
    waypoints = len(reached)

    # print number of waypoints
    print('N', waypoints)

    # if there is no path, restart program
    if len(reached) == 0:
        print("no path, please try again. program will now end")
        sys.exit()

    # for each waypoint in the shortest path, get the waypoint's coordinates
    # and then only print it if a valid request/input is processed
    for point in reached:
        (lat, lon) = location[point]
        checkinput()

    # indicate that user has reached end of the path
    print('E')
