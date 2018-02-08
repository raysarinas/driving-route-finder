from graph import Graph
from binary_heap import BinaryHeap

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

reached = {}
events = BinaryHeap()
events.insert(start, 0)


while len(events) > 0:
    (u, v), time = events.popmin()
    if v not in reached:
        u = reached[v]
        for: #each neighbour w of v
            events.insert((v, w), time + cost(v, w))

return reached
