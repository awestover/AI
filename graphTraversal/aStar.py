# A*
# use heuristic to make graph traversal faster, but not gaurenteed to be correct
# basically just need to change the sorting in the BinaryHeap (sort by acutally distance + heuristic (guess at remaining distance)
from BinaryHeap import BinaryHeap
import numpy as np
import matplotlib.pyplot as plt

# classic graph theory algorithm
# -1 means not reachable

# then use these for euclidean distance calculuation to get heuristics
# Note: weights need to be dependent on this...

import json
with open('bigGraph.json', 'r') as f:
    data = json.load(f)
node_coordinates = data["nodes"]

plt.gca().invert_yaxis()
plt.scatter([node_coord[1] for node_coord in node_coordinates], [node_coord[0] for node_coord in node_coordinates])
plt.show()

sparse_graph = data["sparse_graph"]
start = 0
N = len(sparse_graph)
goal = N-1
print(N)

ct = 0
plt.gca().invert_yaxis()

with open('maze.json', 'r') as f:
    walls = json.load(f)
plt.imshow(walls)

wantReallySlowButCoolPicture = False
if wantReallySlowButCoolPicture:
    for i in range(N):
        # plt.scatter([node_coordinates[i][1]], [node_coordinates[i][0]], c='b')
        for connection in sparse_graph[i]["indexes"]:
            ct += 1
            plt.plot([node_coordinates[i][1], node_coordinates[connection][1]], [node_coordinates[i][0], node_coordinates[connection][0]], c='white')

print(ct)
plt.show()

def euclideanHeuristic(i):
    dx = abs(node_coordinates[i][0] - node_coordinates[goal][0])
    dy = abs(node_coordinates[i][1] - node_coordinates[goal][1])
    return (dx*dx+dy*dy)**0.5

def manhattanHeuristic(i):
    dx = abs(node_coordinates[i][0] - node_coordinates[goal][0])
    dy = abs(node_coordinates[i][1] - node_coordinates[goal][1])
    return dx+dy

class Node:
    def __init__(self, index):
        self.index = index

    def getValue(self):
        return dists[self.index] + manhattanHeuristic(self.index)

    def __str__(self):
        return "index: {}, dists: {}".format(self.index, dists[self.index])

heap = BinaryHeap()

dists = [0] + [float('inf') for i in range(N-1)] # distances from the start node (start node is distance 0 from itself)
best_paths = [[] for i in range(N)]
heap.insert(Node(0))
nodesExplored = 0
while heap.findMin().index != goal:
    nodesExplored += 1
    curMinIdx = heap.findMin().index
    connections = sparse_graph[curMinIdx] # don't store the non-existent connections in the sparse representation of the graph
    # travel to every connection that is not -1 leading out of it (note that every edge is an arrow going both ways so the adjacency matrix is symmetric)
    for i in range(len(connections["indexes"])):
        new_distance = connections["values"][i] + dists[curMinIdx]
        if new_distance < dists[connections["indexes"][i]]:
            dists[connections["indexes"][i]] = new_distance
            best_paths[connections["indexes"][i]] = best_paths[curMinIdx] + [curMinIdx]
            heap.insert(Node(connections["indexes"][i])) # potential bug: Am I inserting things multiple times?
    heap.deleteMin()
    print(heap)

print("best path: {}, distance: {}".format(best_paths[goal], dists[goal]))

toPlot = {"x": [], "y": []}
for node in best_paths[goal]+[goal]:
    toPlot["x"].append(node_coordinates[node][1])
    toPlot["y"].append(node_coordinates[node][0])
print(node_coordinates)

plt.gca().invert_yaxis()
plt.imshow(walls)
plt.plot(toPlot["x"], toPlot["y"], c='white')
plt.show()

# note: better performance with manhattanHeuristic
print(nodesExplored)
