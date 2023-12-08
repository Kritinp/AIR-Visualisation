import networkx as nx
import matplotlib.pyplot as plt
import os 
import subprocess
import time
def delete_files_in_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                # print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error: {e}")

folder_path1 = '/home/kritin/College/SDS/Project/dashboard/src/buffers'
folder_path2 = '/home/kritin/College/SDS/Project/dashboard/src/general'
delete_files_in_folder(folder_path1)
delete_files_in_folder(folder_path2)

time.sleep(5)

    
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

npm_command = "npm run dev"
directory_path = "/home/kritin/College/SDS/Project/dashboard"

try:
    subprocess.run(npm_command, shell=True, check=True, cwd=directory_path)
except subprocess.CalledProcessError as e:
    print(f"Error executing '{npm_command}' in '{directory_path}': {e}")
