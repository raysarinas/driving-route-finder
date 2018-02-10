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
        print("Loop 1")
        vertices, time = events.popmin()
        print(type(vertices))
        print(type(vertices[0]))
        if vertices[1] not in reached:
            reached[vertices[1]] = vertices[0]# vertices[0] = reached[vertices[1]]   burn vertex v, record predecessor u
            for n in graph.neighbours(vertices[1]):
                 # new event: edge (v,w) started burning
                print("Loop 2")
                events.insert(([vertices[1]], n), time + cost.distance((vertices[1], n)))

            if vertices[1] == dest:
                break

    #return reached
    print("Done")
    #find path to see if a path exists
    # return empty list if dest cannot be reached/if no path from start to dest exists
    if dest not in reached:
      return []

    # if the destination gets reached we can form a minimum path

    current = dest
    path = [current]

    while current != start:
        # print("Loop 3")
        print(dest)
        print(type(dest))
        current = reached[current]
        #current = reached[current]
        path.append(current)

    #or while reached[current] != start:
    #path.append(reached[current])
    #    current = reached[current]

    path = path[::-1]
    return path
