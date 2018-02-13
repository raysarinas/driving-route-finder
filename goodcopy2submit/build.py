from graph import Graph

def load_edmonton_graph(filename):
    """
    Loads the graph of Edmonton from the given file.
    Returns two items
      graph: the instance of the class Graph() corresponding to the
        directed graph from edmonton-roads-2.0.1.txt
      location: a dictionary mapping the identifier of a vertex to
        the pair (lat, lon) of geographic coordinates for that vertex.
        These should be integers measuring the lat/lon in 100000-ths
        of a degree.
    In particular, the return statement in your code should be
      return graph, location
    (or whatever name you use for the variables).
    Note: the vertex identifiers should be converted to integers
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
