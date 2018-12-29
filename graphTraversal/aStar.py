# A*
# use heuristic to make graph traversal faster, but not gaurenteed to be correct
# basically just need to change the sorting in the BinaryHeap (sort by acutally distance + heuristic (guess at remaining distance)
# from BinaryHeap import BinaryHeap
import numpy as np
import matplotlib.pyplot as plt

# classic graph theory algorithm
# -1 means not reachable

# then use these for euclidean distance calculuation to get heuristics
# Note: weights need to be dependent on this...

import json
with open('data/bigGraph.json', 'r') as f:
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

with open('data/maze.json', 'r') as f:
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

# this is a min-heap (root is smallest element)
class BinaryHeap():
    def __init__(self):
        self.nodes = []
        self.length = 0

    def insert(self, node):
        # put it in at the bottom
        self.nodes.append(node)
        self.length += 1
        self.orderEnsuranceUp(self.length-1)

    # compare and swap with parent if it is smaller than the parent
    def orderEnsuranceUp(self, i):
        if i > 0:
            parentIdx = self.getParent(i)
            if self.nodes[i].getValue() < self.nodes[parentIdx].getValue():
                self.swap(i, parentIdx)
                self.orderEnsuranceUp(parentIdx)

    # compare and swap with smallest child if it is bigger than the child
    def orderEnsuranceDown(self, i):
        leftChildIdx = self.getLeftChild(i)
        rightChildIdx = leftChildIdx + 1
        if leftChildIdx < self.length:
            smallChildIdx = leftChildIdx
            if rightChildIdx < self.length:
                if self.nodes[rightChildIdx].getValue() < self.nodes[leftChildIdx].getValue():
                    smallChildIdx = rightChildIdx

            if self.nodes[smallChildIdx].getValue() < self.nodes[i].getValue():
                self.swap(smallChildIdx, i)
                self.orderEnsuranceDown(smallChildIdx)

    def deleteMin(self):
        heapNodeIndexes[self.nodes[0].index] = None
        self.nodes[0] = self.nodes[self.length - 1]
        heapNodeIndexes[self.nodes[0].index] = 0

        self.length -= 1
        self.nodes.pop()
        self.orderEnsuranceDown(0)

    def swap(self, i, j):
        tmp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = tmp

        tmp = heapNodeIndexes[self.nodes[i].index]
        heapNodeIndexes[self.nodes[i].index] = heapNodeIndexes[self.nodes[j].index]
        heapNodeIndexes[self.nodes[j].index] = tmp

    def findMin(self):
        return self.nodes[0]

    def getParent(self, idx):
        return (idx - 1)//2

    def getLeftChild(self, idx):
        return idx*2+1

    def isEmpty(self):
        return self.length == 0

    def __str__(self):
        return " \t".join([nodeI.__str__() for nodeI in self.nodes])


heap = BinaryHeap()

# dists = [0] + [float('inf') for i in range(N-1)] # distances from the start node (start node is distance 0 from itself)
dists = []
heapNodeIndexes = [] # index into the heap to get that node
for i in range(N):
    if i == start:
        dists.append(0)
    else:
        dists.append(float('inf'))
    heap.insert(Node(i))
    heapNodeIndexes.append(i)

best_paths = [[] for i in range(N)]
# heap.insert(Node(0))
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
            # for i in range(len(heap.nodes)):
                # heap.orderEnsuranceUp(i)
            heap.orderEnsuranceUp(heapNodeIndexes[connections["indexes"][i]])
    heap.deleteMin()

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
