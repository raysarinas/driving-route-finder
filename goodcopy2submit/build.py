from graph import Graph

def load_edmonton_graph(filename):
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        for line in filename:
            row = line.strip().split(",")

            if row[0] == "V":
                graph.add_vertex(int(row[1]))
                latitude = int(float(row[2]) * 100000)
                longitude = int(float(row[3]) * 100000)
                location[int(row[1])] = (latitude, longitude)

            elif row[0] == "E":
                graph.add_edge((int(row[1]), int(row[2])))

    return graph, location
