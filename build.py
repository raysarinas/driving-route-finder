from graph import Graph
from breadth_first_search import breadth_first_search

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

def count_components(agraph):
    '''
        returns the number of connected components in a graph supplied
        by the argument of the function.

        args:
            agraph - graph that has connected components

        return:
            int - integer number of the connected components in agraph
    '''
    vertices = agraph.get_vertices()
    num_components = 0

    while vertices:
        checking = vertices.pop()
        justvisited = breadth_first_search(agraph, checking)
        vertices = [v for v in vertices if v not in justvisited]
        num_components += 1

    return num_components

def read_city_graph_undirected(filename):
    '''
        returns an undirected graph of the class Graph from a text file
        describing a road network.

        args:
            filename - name of text file that is used to create an instance
                       of an undirected graph

        return:
            Graph - returns an undirected graph of the city of a road network
    '''
    with open(filename, 'r') as filename:
        undirected_graph = Graph()

        for line in filename:
            row = line.strip().split(",")
            if row[0] == "V":
                undirected_graph.add_vertex(row[1])
            elif row[0] == "E":
                undirected_graph.add_edge((row[1], row[2]))
                undirected_graph.add_edge((row[2], row[1]))

    return undirected_graph
