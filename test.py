import networkx as nx
import matplotlib.pyplot as plt
import mplcursors

def update_node_info(new_info):
    global node_info
    node_info = new_info
    
    plt.clf()
    pos = nx.shell_layout(G, [[node for node in G.nodes()]])
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')
    
    nx.draw_networkx_labels(G, pos, labels=node_info)
    
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", on_hover)
    
    plt.show()

def on_hover(sel):
    node = sel.target.index
    sel.annotation.set_text(node_info.get(node, "No information"))

G = nx.Graph()

# Read the edges from the file
with open("/home/kritin/College/SDS/Project/dashboard/src/general/edges.txt", "r") as file:
    for line in file:
        edge = line.strip().split(',')
        if len(edge) == 2:
            G.add_edge(int(edge[0]), int(edge[1]))

# Generate node information (dummy information for demonstration)
node_info = {node: f"Node {node} Information" for node in G.nodes()}

# Plotting the graph
pos = nx.shell_layout(G, [[node for node in G.nodes()]])
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')

cursor = mplcursors.cursor(hover=True)
cursor.connect("add", on_hover)

plt.show()

# Uncomment the following lines to update node information and redraw the graph
# new_node_info = {
#     1: "Updated Node 1 Information",
#     2: "Updated Node 2 Information",
#     ...
# }
# update_node_info(new_node_info)
