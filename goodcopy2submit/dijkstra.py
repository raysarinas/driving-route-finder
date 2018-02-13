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
