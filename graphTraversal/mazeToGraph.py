import matplotlib.pyplot as plt
import json
with open('data/maze.json', 'r') as f:
    walls = json.load(f)
# with open('data/smallMaze.json', 'r') as f:
#     walls = json.load(f)

plt.imshow(walls)
plt.show()

N = len(walls)

def count_neighbors(i, j):
    neighbor_ct = 0
    for ii in [-1, 0, 1]:
        for jj in [-1, 0, 1]:
            if ii != 0 or jj != 0:
                if i + ii >= 0 and i + ii <= N-1:
                    if j + jj >= 0 and j + jj <= N-1:
                        if not walls[i+ii][j+jj]:
                            neighbor_ct += 1
    return neighbor_ct

# ASSUMING: the point is not on the outer edge! (walls arround the outside is the assumption)
def isCorner(i, j):
    if walls[i][j] == 1:
        return False
    dirrections = [([-1,0],[0,1]),([-1,0],[0,-1]),([1,0],[0,1]),([1,0],[0,-1])]
    for wallPair in dirrections:
        if walls[i+wallPair[0][0]][j+wallPair[0][1]] and walls[i+wallPair[1][0]][j+wallPair[1][1]]:
            return True
    return False

corners = [[0 for j in range(N)] for i in range(N)]

corner_coords = []

num_corners = 0
for i in range(N):
    for j in range(N):
        if not walls[i][j]:
            if isCorner(i, j) or count_neighbors(i, j) > 2:
                corners[i][j] = 1
                num_corners += 1
                corner_coords.append([i,j])
plt.imshow(corners)
plt.show()

# connection criterion:
# there must be a straight shot (equal i or equal j) from the first one to the second one,
# AND there can not be any walls along the straight shot

print(num_corners)
sparse_graph = [{"indexes": [], "values": []} for i in range(num_corners)] # there are way too many corners to do an adjacency matrix that is num_corners by num_corners, so we do a compressed representation
# my convention is sparse_graph[i] = {"indexes": [j0,j1,...], "values": [distances from i to j0, j1, ...]}

connections = 0
for i in range(num_corners-1):
    for j in range(i+1, num_corners):
        if corner_coords[i][0] == corner_coords[j][0]:
            bothI = corner_coords[i][0]
            leftCorner = min(corner_coords[i][1], corner_coords[j][1])
            rightCorner = max(corner_coords[i][1], corner_coords[j][1])
            hasWalls = False
            for jj in range(leftCorner+1, rightCorner):
                if walls[bothI][jj]:
                    hasWalls = True
                    break
            if not hasWalls:
                sparse_graph[i]["indexes"].append(j)
                sparse_graph[i]["values"].append(rightCorner - leftCorner)
                sparse_graph[j]["indexes"].append(i)
                sparse_graph[j]["values"].append(rightCorner - leftCorner)
                connections += 1
        if corner_coords[i][1] == corner_coords[j][1]:
            bothJ = corner_coords[i][1]
            topCorner = min(corner_coords[i][0], corner_coords[j][0])
            bottomCorner = max(corner_coords[i][0], corner_coords[j][0])
            hasWalls = False
            for ii in range(topCorner+1, bottomCorner):
                if walls[ii][bothJ]:
                    hasWalls = True
                    break
            if not hasWalls:
                sparse_graph[i]["indexes"].append(j)
                sparse_graph[i]["values"].append(rightCorner - leftCorner)
                sparse_graph[j]["indexes"].append(i)
                sparse_graph[j]["values"].append(rightCorner - leftCorner)
                connections += 1
print(connections)
with open('data/bigGraph.json', 'w') as f:
    json.dump({"sparse_graph": sparse_graph, "nodes": corner_coords}, f)
