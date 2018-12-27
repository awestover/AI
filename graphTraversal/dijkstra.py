
from BinaryHeap import BinaryHeap
from Node import Node

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

# GOAL: get from node 0 to node 6
start = 0
goal = 6
N = len(test_graph)

heap = BinaryHeap()

# pseudocode
"""
dists = [0] + [float('inf') for i in range(N-1)] # distances from the start node (start node is ditance 0 from itself)
put 0 in the heap (need to put the index in the heap with the value which is the distnace, will have to modify the heap class so that this is possible)
while top of the heap is not the goal node:
    get the node from the top of the heap
    # travel to every connection that is not -1 leading out of it (note that every edge is an arrow going both ways so the adjacency matrix is symetric)
    for each connection that is not -1:
        compute distance through current node to this node
        see if that is smaller than the current distane recorded in dists
        if it is a shorter path:
            change the distance entry so that it says that it is shorter
            insert this node in the heap # QUESTION: do we have to worry about a node being in the heap multiple times? We could have a variable 'visited' or something for each node that indicates if it is in the heap already if this is necessary...
    heap.deleteMin()
"""
dists = [0] + [float('inf') for i in range(N-1)] # distances from the start node (start node is distance 0 from itself)
heap.insert(Node(0))
while heap.findMin().index != goal:
    curMinIdx = heap.findMin().index
    connections = test_graph[curMinIdx]
    real_connections = [{"index": i, "distance": connections[i]} for i in range(len(connections)) if connections[i] != -1]
    # travel to every connection that is not -1 leading out of it (note that every edge is an arrow going both ways so the adjacency matrix is symmetric)
    for connection in real_connections:
        new_distance = connection["distance"] + dists[curMinIdx]
        if new_distance < dists[connection["index"]]:
            dists[connection["index"]] = new_distance
            heap.insert(Node(connection["index"]))# potential bug: Am I inserting things multiple times?
    heap.deleteMin()
    print(heap)
