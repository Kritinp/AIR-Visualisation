import networkx as nx
import matplotlib.pyplot as plt
import mplcursors 

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

node_info = {1: "Node 1 Information", 2: "Node 2 Information", 3: "Node 3 Information", 4: "Node 4 Information"}

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')

def update_node_info(new_info):
    global node_info  
    node_info = new_info
    
    plt.clf()  
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')
    
    nx.draw_networkx_labels(G, pos, labels=node_info)

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", on_hover)

    plt.show()

def on_hover(sel):
    node = sel.target.index
    sel.annotation.set_text(node_info.get(node, "No information"))

cursor = mplcursors.cursor(hover=True)
cursor.connect("add", on_hover)

plt.show()

# new_node_info = {
#     1: "Updated Node 1 Information",
#     2: "Updated Node 2 Information",
#     3: "Updated Node 3 Information",
#     4: "Updated Node 4 Information"
# }

# Update the graph with new information
# update_node_info(new_node_info)
