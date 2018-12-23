# Author: Alek Westover
# Purpose: generate a map
# Source: wikipedia on map generation
"""
Idea: start with a grid. Each cell has 4 walls and is initially unvisited
by the end every cell in the grid will be visited.
Algorithm:

Initialize the starting cell as visited,
set it as the current cell,
and add it to a stack of visited locations for backtracking

while there are unvisited cells:
    if the current cell has unvisited neighbors:
        choose one at random
        delete the wall between the current cell and the chosen neighbor
        add the neighbor to the stack of visited locations for backtracking
        set the neighbor cell as visited
        set the neighbor to the current cell
    elif the stack is not empty:
        pop the top off of the stack
        set the new top of the stack as the current cell
"""

import random

N = 30

def get_unvisited_neighbors(grid, idx):
    unvisited_neighbors = []
    if idx[0] != 0:
        if not grid[idx[0]-1][idx[1]]:
            unvisited_neighbors.append({"wall": "i", "idx":[idx[0]-1,idx[1]], "wallIdx":[idx[0],idx[1]]})
    if idx[0] != N-1:
        if not grid[idx[0]+1][idx[1]]:
            unvisited_neighbors.append({"wall": "i", "idx":[idx[0]+1,idx[1]], "wallIdx":[idx[0]+1,idx[1]]})
    if idx[1] != 0:
        if not grid[idx[0]][idx[1]-1]:
            unvisited_neighbors.append({"wall": "j", "idx":[idx[0],idx[1]-1], "wallIdx":[idx[0],idx[1]]})
    if idx[1] != N-1:
        if not grid[idx[0]][idx[1]+1]:
            unvisited_neighbors.append({"wall": "j", "idx":[idx[0],idx[1]+1], "wallIdx":[idx[0],idx[1]+1]})
    return unvisited_neighbors

grid = [[False for j in range(N)] for i in range(N)] # whether or not the cells have been visited
Iwalls = [[True for j in range(N)] for i in range(N+1)] # block movement in the "i" (up down) dirrection
Jwalls = [[True for j in range(N+1)] for i in range(N)]

grid[0][0] = True
current_cell = [0,0]
backtracking_stack = [current_cell[:]]

visitedCt = 1

while visitedCt < N*N:
    unvisited_neighbors = get_unvisited_neighbors(grid, current_cell)
    if len(unvisited_neighbors) > 0:
        neighbor = random.choice(unvisited_neighbors)
        if neighbor["wall"] == "i":
            Iwalls[neighbor["wallIdx"][0]][neighbor["wallIdx"][1]] = False
        else:
            Jwalls[neighbor["wallIdx"][0]][neighbor["wallIdx"][1]] = False
        backtracking_stack.append(neighbor["idx"][:])
        current_cell = neighbor["idx"]
        grid[current_cell[0]][current_cell[1]] = True
        visitedCt += 1
    elif len(backtracking_stack) > 0:
        backtracking_stack.pop()
        if len(backtracking_stack) != 0:
            current_cell = backtracking_stack[-1]

import matplotlib.pyplot as plt
for i in range(N):
    for j in range(N+1):
        if Jwalls[i][j]:
            plt.plot([j,j],[i,i+1], 'r')

for i in range(N+1):
    for j in range(N):
        if Iwalls[i][j]:
            plt.plot([j,j+1],[i,i], 'b')

# plot it, cell is a unit grid
plt.show()
