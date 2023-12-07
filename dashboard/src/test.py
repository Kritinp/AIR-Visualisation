import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Set to store unique edges
edges_set = set()

# Read the edges from the file and add unique edges to the graph
with open("/home/kritin/College/SDS/Project/dashboard/src/general/edges.txt", "r") as file:
    for line in file:
        edge = tuple(sorted(map(int, line.strip().split(','))))
        if len(edge) == 2 and edge not in edges_set:
            edges_set.add(edge)
            G.add_edge(*edge)

# Generate node information (dummy information for demonstration)
node_info = {node: f"Node {node} Information" for node in G.nodes()}

# Plotting the graph
pos = nx.shell_layout(G, [[node for node in G.nodes()]])
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')

plt.savefig('/home/kritin/College/SDS/Project/dashboard/src/assets/graph.png')  # Save the graph as an image file
# plt.show()  # Uncomment if you also want to display the graph

