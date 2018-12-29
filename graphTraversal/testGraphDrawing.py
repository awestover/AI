import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()
for i in range(4):
    G.add_node(i)

G.add_edge(0,3)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,1)

print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())

nx.draw(G)
plt.savefig("simple_path.png") # save as png
plt.show() # display

import json
with open('bigGraph.json', 'r') as f:
    data = json.load(f)

for node in data["nodes"]:
    plt.scatter(node[0], node[1])
plt.show()
