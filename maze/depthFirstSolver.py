
# this is the champion solver, because it can solve even mazes that aren't simply connected!

import matplotlib.pyplot as plt
import random
import json
with open('grid.json', 'r') as f:
    wallMatrix = json.load(f)

N = len(wallMatrix)
grid = [[0 for j in range(N)] for i in range(N)] # keep track of how many times each cell has been visited

current_cell = [0, 0]
end_cell = [N-1, N-1]

def at_cell(current_cell, other_cell):
    return current_cell[0] == other_cell[0] and current_cell[1] == other_cell[1]

def grid_at(cell):
    return grid[cell[0]][cell[1]]

def visit_grid_cell(cell):
    grid[cell[0]][cell[1]] += 1

def walls_at(cell):
    return wallMatrix[cell[0]][cell[1]]

def get_unblocked_neighbors(current_cell):
    cWalls = walls_at(current_cell)
    unblocked_neighbors = []

    if not cWalls[0]: # right
        unblocked_neighbors.append([current_cell[0], current_cell[1]+1])
    if not cWalls[1]: # up
        unblocked_neighbors.append([current_cell[0]-1, current_cell[1]])
    if not cWalls[2]: # left
        unblocked_neighbors.append([current_cell[0], current_cell[1]-1])
    if not cWalls[3]: # down
        unblocked_neighbors.append([current_cell[0]+1, current_cell[1]])

    return unblocked_neighbors

backtracking_stack = [current_cell[:]]

for i in range(N):
    for j in range(N):
        if wallMatrix[i][j][0]: # right
            plt.plot([j+1,j+1],[i,i+1],'b')
        if wallMatrix[i][j][1]: # up
            plt.plot([j,j+1],[i,i],'b')
        if wallMatrix[i][j][2]: # left
            plt.plot([j,j],[i,i+1],'b')
        if wallMatrix[i][j][3]: # down
            plt.plot([j,j+1],[i+1,i+1],'b')

plt.gca().invert_yaxis()
plt.pause(0.1)


while not at_cell(current_cell, end_cell):
    unblocked_neighbors = get_unblocked_neighbors(current_cell)
    unblocked_neighbor_visits = [grid_at(neighborI) for neighborI in unblocked_neighbors]
    correct_visits = min(unblocked_neighbor_visits)
    if correct_visits == 2:
        print("The maze is not solvable!")
        break
    elif correct_visits == 1:
        if len(backtracking_stack) > 2:
            backtracking_stack.pop()
            current_cell = backtracking_stack[-1][:]
            plt.scatter(current_cell[1]+0.5, current_cell[0]+0.5, c='b')
        else:
            print("I am pretty sure the maze is not solvable")
            break
    else: # correct_visits == 0
        correct_visits_neighbors = []
        for i in range(len(unblocked_neighbor_visits)):
            if unblocked_neighbor_visits[i] == correct_visits:
                correct_visits_neighbors.append(unblocked_neighbors[i])

        current_cell = random.choice(correct_visits_neighbors)
        visit_grid_cell(current_cell)
        backtracking_stack.append(current_cell[:])
        plt.scatter(current_cell[1]+0.5, current_cell[0]+0.5, c='r')

    if random.random() < 0.1:
        plt.pause(0.01)
