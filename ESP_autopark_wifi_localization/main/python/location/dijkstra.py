import sys


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        """
        This method makes sure that the graph is symmetrical.
        In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        """
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]
    
    
def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
        # However, we initialize the starting node's value with 0
        shortest_path[start_node] = 0

        # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path



def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))


nodes = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12", "n13", "n14", "n15", "n16", "n17", "n18", "n19"]
init_graph = {}
for node in nodes:
    init_graph[node] = {}

init_graph["n1"]["n2"] = 21.93
init_graph["n1"]["n17"] = 23.85

init_graph["n2"]["n3"] = 27.3
init_graph["n2"]["n17"] = 22
init_graph["n2"]["s2"] = 27

init_graph["n3"]["n4"] = 21
init_graph["n4"]["s3"] = 24
init_graph["n4"]["n5"] = 24

init_graph["n5"]["s4"] = 24
init_graph["n5"]["n19"] = 34.21
init_graph["n5"]["n6"] = 26

init_graph["n6"]["s5"] = 24
init_graph["n6"]["n7"] = 25
init_graph["n6"]["n19"] = 27.46

init_graph["n7"]["s6"] = 24
init_graph["n7"]["n8"] = 25
init_graph["n8"]["n9"] = 27.07


init_graph["n9"]["s7"] = 24
init_graph["n9"]["n10"] = 22
init_graph["n10"]["s8"] = 24
init_graph["n10"]["n11"] = 22.1

init_graph["n11"]["n12"] = 25
init_graph["n12"]["s9"] = 25
init_graph["n12"]["n13"] = 25

init_graph["n13"]["s10"] = 25
init_graph["n13"]["n14"] = 26
init_graph["n13"]["n18"] = 22.56

init_graph["n14"]["s11"] = 25
init_graph["n14"]["n18"] = 30.41
init_graph["n14"]["n15"] = 24

init_graph["n15"]["s12"] = 25
init_graph["n15"]["n16"] = 21
init_graph["n16"]["n17"] = 22.36
init_graph["n17"]["s1"] = 27

init_graph["n18"]["s1"] = 35
init_graph["n18"]["s8"] = 33
init_graph["n18"]["n19"] = 22
init_graph["n19"]["s2"] = 35
init_graph["n19"]["s7"] = 33

graph = Graph(nodes, init_graph)
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="n1")
print("From n1 to s8:")
print_result(previous_nodes, shortest_path, start_node="n1", target_node="s8")

print("\n")
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="s8")
print("From s8  to s3:")
print_result(previous_nodes, shortest_path, start_node="s8", target_node="s3")

# The examples above are run based on values where there are no cars or obstacles in the parking area.