from graph import Graph
from binary_heap import BinaryHeap
import math
import sys

def least_cost_path(graph, start, dest, cost):
    """Find and return a least cost path in graph from start vertex to dest vertex.
    Efficiency: If E is the number of edges, the run-time is
      O( E log(E) ).
    Args:
      graph (Graph): The digraph defining the edges between the
        vertices.
      start: The vertex where the path starts. It is assumed
        that start is a vertex of graph.
      dest:  The vertex where the path ends. It is assumed
        that dest is a vertex of graph.
      cost:  A class with a method called "distance" that takes
        as input an edge (a pair of vertices) and returns the cost
        of the edge. For more details, see the CostDistance class
        description below.
    Returns:
      list: A potentially empty list (if no path can be found) of
        the vertices in the graph. If there was a path, the first
        vertex is always start, the last is always dest in the list.
        Any two consecutive vertices correspond to some
        edge in graph.
        """

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

    # IMPLEMENTED FROM GET_PATH FUNCTION FROM breadth_first_search
    # finds minimum path
    # start at the dest and continuosly and find the parent of current vertex
    # until have reached starting vertex
    current = dest
    path = [current]

    while current != start:
        current = reached[current]
        path.append(current)

    path = path[::-1]
    return path


def load_edmonton_graph(filename):
    """
    Loads the graph of Edmonton from the given file.
    Args:
      filename: file to be read and used to create an instance of a
                Graph object.
    Returns two items:
      graph: the instance of the class Graph() corresponding to the
        directed graph from edmonton-roads-2.0.1.txt
      location: a dictionary mapping the identifier of a vertex to
        the pair (lat, lon) of geographic coordinates for that vertex.
        These should be integers measuring the lat/lon in 100000-ths
        of a degree.

    Note: the vertex identifiers are converted to integers
      before being added to the graph and the dictionary.
     """

    # get the file and open it
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        # split at each comma and store data appropriately
        for line in filename:
            row = line.strip().split(",")

            # if first character is a 'V' store vertex data
            # elif first character is an 'E' store edge data
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
    """
    Creates an instance of the CostDistance class and stores the
    dictionary "location" as a member of this class.
    """
    def __init__(self, location):
        """
        Creates an instance of the CostDistance class and stores the
        dictionary "location" as a member of this class.
        """
        self.locDict = location

    def distance(self, e):
        """
        Here e is a pair (u,v) of vertices.
        Returns the Euclidean distance between the two vertices u and v.
        """
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]

        # calculate the Euclidean distance between two points(x1,y1) and (x2,y2)
        e_dist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
        return e_dist


def checkrequest(validrequest):
    """
    Check if request character is valid i.e. is equal to the character 'R'.
    If the request is not valid not, exit the program.

    Args:
    validrequest: first character that is taken from the user input.

    Doesn't return anything.
    """
    if validrequest != 'R':
        print("try again pls input something else thanks bye")
        sys.exit()


def euc_dist(point, coord):
    """
    Args: point and coord are tuples that contain coordinates.
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

    Args:
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
