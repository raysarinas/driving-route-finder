from graph import Graph
# from breadth_first_search import breadth_first_search

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
        # filename = 'edmonton-roads-2.0.1.txt'

        with open(filename, 'r') as filename:
            graph = Graph()
            location = {}

            for line in filename:
                row = line.strip().split(",")

                if row[0] == "V":
                    graph.add_vertex(row[1])
                    latitude = int((row[2])*100000)
                    longitude = int((row[3])*100000)
                    location[row[1]] = [latitude, longitude]
                    
                elif row[0] == "E":
                    graph.add_edge((row[1], row[2]))
                    graph.add_edge((row[2], row[1]))

        return graph, location
