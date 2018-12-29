from BinaryHeap import BinaryHeap

# classic graph theory algorithm
# -1 means not reachable
test_graph = [
    [-1, 10, 8 , 1 , -1, -1, -1],
    [10, -1, -1, -1, 4 , 9 , -1],
    [8 , -1, -1, -1, 7 , -1, -1],
    [1 , -1, -1, -1, 8 , -1, -1],
    [-1, 4 , 7 , 8 , -1, -1, 7 ],
    [-1, 9 , -1, -1, -1, -1, 6 ],
    [-1, -1, -1, -1, 7 , 6 , -1]
]

class Node:
    def __init__(self, index):
        self.index = index

    def getValue(self):
        return dists[self.index]

    def __str__(self):
        return "index: {}, dists: {}".format(self.index, dists[self.index])


# GOAL: get from node 0 to node 6
start = 0
goal = 6
N = len(test_graph)

heap = BinaryHeap()

# pseudocode
"""
dists = [0] + [float('inf') for i in range(N-1)] # distances from the start node (start node is ditance 0 from itself)
queue everything

while top of the heap is not the goal node:
    get the node from the top of the heap
    # travel to every connection that is not -1 leading out of it (note that every edge is an arrow going both ways so the adjacency matrix is symetric)
    for each connection that is not -1:
        compute distance through current node to this node
        see if that is smaller than the current distane recorded in dists
        if it is a shorter path:
            change the distance entry so that it says that it is shorter
    heap.deleteMin()
"""
dists = [] # distances from the start node (start node is distance 0 from itself)
for i in range(N):
    if i == start:
        dists.append(0)
    else:
        dists.append(float('inf'))
heap.insert(Node(0))

alreadyProcessed = [False for i in range(N)]

best_paths = [[] for i in range(N)]
while heap.findMin().index != goal:
    curMinIdx = heap.findMin().index
    heap.deleteMin()
    if alreadyProcessed[curMinIdx]:
        continue
    else:
        alreadyProcessed[curMinIdx] = True
    connections = test_graph[curMinIdx]
    real_connections = [{"index": i, "distance": connections[i]} for i in range(len(connections)) if connections[i] != -1]
    # travel to every connection that is not -1 leading out of it (note that every edge is an arrow going both ways so the adjacency matrix is symmetric)
    for connection in real_connections:
        new_distance = connection["distance"] + dists[curMinIdx]
        if new_distance < dists[connection["index"]]:
            dists[connection["index"]] = new_distance
            best_paths[connection["index"]] = best_paths[curMinIdx] + [curMinIdx]
            heap.insert(Node(connection["index"])) # Note: sometimes will have multiple of a single node in the heap, the one with minimum distance will be processed first, and its results override everything else
    print(heap)

print("best path: {}, distance: {}".format(best_paths[goal], dists[goal]))
