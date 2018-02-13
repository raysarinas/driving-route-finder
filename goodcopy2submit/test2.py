#   Assignment 1 Part 1
#   By Jesse Goertzen (1505959) and Navras Kamal (1505463)

import math  # For math.sqrt()
from graph import Graph
from binary_heap import BinaryHeap


# Modified solution to Exercise 3 by Jesse Goertzen
def load_edmonton_graph(filename):
    g = Graph()
    location = dict()

    # Open the data file
    graphFile = open(filename, 'r')
    lines = graphFile.readlines()

    for line in lines:
        # Split at each comma, data stored comma-separated
        line = line.split(',')

        # Depending on the first character, treat input as vertex or edge
        if line[0] == 'V':  # Vertex
            # Add the vertex to the graph, and store the coordinates of the vertex
            g.add_vertex(int(line[1]))
            coords = (int(float(line[2]) * 100000), int(float(line[3]) * 100000))
            location[int(line[1])] = coords

        if line[0] == 'E':  # Edge
            g.add_edge((int(line[1]), int(line[2])))

    # Don't forget to close the file!
    graphFile.close()

    return g, location


def get_path(reached, start, end):
    #  get_path function provided in the useful functions tar file

    if end not in reached:
        return []  # unreachable

    # Build the path in reverse order, starting at the end
    path = [end]

    while end != start:
        end = reached[end]  # step to the vertex old end was reached by
        path.append(end)  # add to the path

    path.reverse()  # reverse the path to go from start to end
    return path


class CostDistance:
    # Class used to store the location dict which contains the coordinates of each vertex
    def __init__(self, location):
        # Initialize an instance of the class with the locations of the graph
        self.locations = location

    # e is a pair of vertices (u, v)
    # return the Euclidean distance between the two
    def distance(self, e):
        start, end = self.locations[e[0]], self.locations[e[1]]  # Get coordinates of start and end
        xdiff, ydiff = ((start[0] - end[0])**2), ((start[1] - end[1])**2)
        return math.sqrt(xdiff + ydiff)

    # distance from an arbitrary point to a vertex in the graph
    # v is a key for a vertex in the graph, r is a tuple of coordinates
    def dist2Vertex(self, v, r):
        start, end = r, self.locations[v]
        xdiff, ydiff = ((start[0] - end[0])**2), ((start[1] - end[1])**2)
        return math.sqrt(xdiff + ydiff)


def least_cost_path(graph, start, dest, cost):
    # Implementation of Dijkstra's algorithm
    events = BinaryHeap()
    reached = dict()
    events.insert((start, start), 0)  # Begin at time 0, at the start vertex

    while events:
        edge, time = events.popmin()  # Get next burnt vertex
        if edge[1] not in reached:  # If the destination is not been reached
            reached[edge[1]] = edge[0]  # Keep track of where we came from
            for w in graph.neighbours(edge[1]):  # Burn the neighbours!!!!
                events.insert(((edge[1]), w), (time + cost.distance((edge[1], w))))  # Add the fuse

    return get_path(reached, start, dest)  # return the path


# Simple function to check the validity of the acknowledgement from the user/arduino
def checkRcpt():
    rcpt = input()
    if rcpt != "A":
        raise inputError('Invalid Receipt')
    else:
        return True


if __name__ == "__main__":
    # Load the graph and read the input request
    edmonton_graph, location = load_edmonton_graph("edmonton-roads-2.0.1.txt")
    request = input()
    request = request.split(' ')
    cost = CostDistance(location)

    # Ensure a valid request
    if request[0] != "R":
        raise inputError('Invalid request format.')

    # Read coordinates of the start and destination
    start = (int(request[1]), int(request[2]))
    end = (int(request[3]), int(request[4]))

    minStart, minEnd = float('inf'), float('inf')
    startKey, endKey = -1, -1

    # Find the nearest vertex to the start and destination request
    for v in location:
        diffStart, diffEnd = cost.dist2Vertex(v, start), cost.dist2Vertex(v, end)
        if diffStart < minStart:
            minStart, startKey = diffStart, v
        if diffEnd < minEnd:
            minEnd, endKey = diffEnd, v

    # Find the shortest path
    path = least_cost_path(edmonton_graph, startKey, endKey, cost)

    print('N', len(path))
    path.reverse()  # reverse to make use of path.pop()

    while path:
        if not checkRcpt():  # break if acknowledgement is invalid
            break
        waypoint = path.pop()
        print('W', location[waypoint][0], location[waypoint][1])

    print('E')
