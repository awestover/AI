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

N = 50

class Cell():
    """the cell class"""
    def __init__(self, idx):
        self.visited = 0
        self.walls = [1, 1, 1, 1]
        # walls are [right, up, left, down]
        self.idx = idx

def get_unvisited_neighbors(grid, idx):
    unvisited_neighbors = []
    if idx[0] != 0:
        if not grid[idx[0]-1][idx[1]].visited:
            unvisited_neighbors.append({"wall": 1, "idx":[idx[0]-1,idx[1]]})
    if idx[0] != N-1:
        if not grid[idx[0]+1][idx[1]].visited:
            unvisited_neighbors.append({"wall": 3, "idx":[idx[0]+1,idx[1]]})
    if idx[1] != 0:
        if not grid[idx[0]][idx[1]-1].visited:
            unvisited_neighbors.append({"wall": 2, "idx":[idx[0],idx[1]-1]})
    if idx[1] != N-1:
        if not grid[idx[0]][idx[1]+1].visited:
            unvisited_neighbors.append({"wall": 0, "idx":[idx[0],idx[1]+1]})
    return unvisited_neighbors

def complement_wall(wall):
    return (wall + 2) % 4

grid = [[Cell([i, j]) for j in range(N)] for i in range(N)]

grid[0][0].visited = 1
current_cell = [0,0]
backtracking_stack = [grid[current_cell[0]][current_cell[1]]]

visitedCt = 1

while visitedCt < N*N:
    unvisited_neighbors = get_unvisited_neighbors(grid, current_cell)
    if len(unvisited_neighbors) > 0:
        neighbor = random.choice(unvisited_neighbors)
        grid[current_cell[0]][current_cell[1]].walls[neighbor["wall"]] = 0
        grid[neighbor["idx"][0]][neighbor["idx"][1]].walls[complement_wall(neighbor["wall"])] = 0
        backtracking_stack.append(grid[neighbor["idx"][0]][neighbor["idx"][1]])
        current_cell = neighbor["idx"]
        grid[current_cell[0]][current_cell[1]].visited = 1
        visitedCt += 1
    elif len(backtracking_stack) > 0:
        backtracking_stack.pop()
        if len(backtracking_stack) != 0:
            current_cell = backtracking_stack[-1].idx

# plot it, cell is a unit grid
import matplotlib.pyplot as plt
for i in range(N):
    for j in range(N):
        if grid[i][j].walls[0]: # right
            plt.plot([j+1,j+1],[i,i+1],'b')
        if grid[i][j].walls[1]: # up
            plt.plot([j,j+1],[i,i],'b')
        if grid[i][j].walls[2]: # left
            plt.plot([j,j],[i,i+1],'b')
        if grid[i][j].walls[3]: # down
            plt.plot([j,j+1],[i+1,i+1],'b')

plt.gca().invert_yaxis()
plt.show()

pixel_grid = [[0 for j in range(3*N)] for i in range(3*N)]
for i in range(N):
    for j in range(N):
        for ii in range(3):
            if pixel_grid[3*i+ii][3*j] == 0:
                pixel_grid[3*i+ii][3*j] = grid[i][j].walls[2] # left
            if pixel_grid[3*i+ii][3*j+2] == 0:
                pixel_grid[3*i+ii][3*j+2] = grid[i][j].walls[0] # right
        for jj in range(3):
            if pixel_grid[3*i][3*j+jj] == 0:
                pixel_grid[3*i][3*j+jj] = grid[i][j].walls[1] # up
            if pixel_grid[3*i+2][3*j+jj] == 0:
                pixel_grid[3*i+2][3*j+jj] = grid[i][j].walls[3] # down
plt.imshow(pixel_grid)
plt.show()

# output the pixel_grid to a file for use in maze solving programs
import json
with open("maze.json", 'w') as f:
    json.dump(pixel_grid, f)

wallMatrix = [[grid[i][j].walls for j in range(N)] for i in range(N)]
with open("grid.json", 'w') as f:
    json.dump(wallMatrix, f)
