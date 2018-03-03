''' SERVER BEING USED FOR PART 2
    I'll put back the docstring comment description thingamobobs later
'''

from graph import Graph
from binary_heap import BinaryHeap
import math
import sys

# modules for python-arduino communication I guess or whatever
from serial import Serial
from time import sleep

def least_cost_path(graph, start, dest, cost):
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

    current = dest
    path = [current]
    while current != start:
        current = reached[current]
        path.append(current)
    path = path[::-1]
    return path


def load_edmonton_graph(filename):
    # get the file and open it
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        # split at each comma and store data appropriately
        for line in filename:
            row = line.strip().split(",")

            # if first character is a 'V' store vertex data, elif 'E' store edge data
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
    def __init__(self, location):
        self.locDict = location

    def distance(self, e):
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]

        # calculate the Euclidean distance between two points(x1,y1) and (x2,y2)
        e_dist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
        return e_dist

def euc_dist(point, coord):
    sum = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
    dist = math.sqrt(sum)

    return dist


def process_input(request, location):
    # store list of input things into appropriate variables
    #valid = request[0]
    start_lat = int(request[1])
    start_lon = int(request[2])
    dest_lat = int(request[3])
    dest_lon = int(request[4])
    startcoord = list()
    destination = list()
    startcoord.append(start_lat)
    startcoord.append(start_lon)
    destination.append(dest_lat)
    destination.append(dest_lon)

    # initialize minimum start/end and start/end vertex values
    minStart = float('inf')
    minEnd = float('inf')
    startV = None
    endV = None

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







if __name__ == "__main__":
	yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
	cost = CostDistance(location)

	with Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1) as ser:
		while True:
            # infinite loop that echoes all messages from
            # the arduino to the terminal
			line = ser.readline()
			line_string = line.decode("ASCII")
			stripped = line_string.rstrip("\r\n")
			print(stripped)

			if not stripped:
    			#timeout and restart loop
				continue

			elif stripped[0] == 'R':
				request = stripped.split()
				print(request)
                # get the start and end vertices
				start, end = process_input(location, request)
				print(start, end)
                # find the shortest path maybe?
                # reached = [] # make empty list but does it rly matter
				reached = least_cost_path(yegGraph, start, end, cost)
				waypoints = len(reached)

				if reached: # if reached is not empty
					waystring = str(waypoints)
					print(waystring)
					num_waypoints = "N " + waystring + "\n"
					print(num_waypoints)
					encoded = num_waypoints.encode("ASCII")
					ser.write(encoded)
					continue

                # might have to change this else statement but not sure
                # if not reached:
				else: # if no vertices reached then no path
					num_waypoints = "N 0\n" # msg to say no waypoints
					encoded = num_waypoints.encode("ASCII") # encode 4 arduino
					ser.write(encoded)

			elif stripped[0] == 'A':
                #if waypoints > 0: # reached
				if reached:
					waypoint = location[reached.pop(0)] # return a list/tuple?
					print(waypoint) # USE THIS TO TEST WHAT IS GETTING RETURNED
					lat, lon = str(waypoint[0]), str(waypoint[1])
					msg = "W " + lat + " " + lon + "\n"
                    #waypoints -= 1

				else: # when finished:
					msg = "E \n"

				encoded = msg.encode("ASCII")
				ser.write(encoded)
				continue # reloop this binch

			else:
    			# something something handshake jacob knows i think
				check = "%"
				encoded = check.encode("ASCII")
				ser.write(encoded)

			sleep(2) # WHY SLEEP??????????????
