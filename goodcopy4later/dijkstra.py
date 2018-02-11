from graph import Graph
from binary_heap import BinaryHeap

def least_cost_path(graph, start, dest, cost):
    reached = {} # empty dictionary
    events = BinaryHeap() # empty heap
    events.insert((start, start), 0) # vertex s burns at time 0

    while len(events) > 0:
        edge, time = events.popmin()
        if edge[1] not in reached:
            reached[edge[1]] = edge[0]
            for nbr in graph.neighbours(edge[1]):
                events.insert((edge[1], nbr), time + cost.distance((edge[1], nbr)))

    if dest not in reached:
      return []

    current = dest
    path = [current]

    while current != start:
        current = reached[current]
        path.append(current)

    path = path[::-1]
    return path
