
# NOTE: this only works for simply connected mazes!
# NOTE: this works for a human in a maze too.

import matplotlib.pyplot as plt
import random

import json
with open('maze.json', 'r') as f:
    pixel_grid = json.load(f)

N = len(pixel_grid)
current_cell = [1, 1]
end_cell = [N-2, N-2]

print(pixel_grid[1][1]) # 0, it is empty
orientation = [0, 1] # go right (+j) initially

def update_cell(current_cell, orientation):
    return [current_cell[0] + orientation[0], current_cell[1] + orientation[1]]

def pixel_grid_at(cell):
    return pixel_grid[cell[0]][cell[1]]

def turn_left(orientation):
    # R90 = [[0,-1],[1,0]]
    return [-orientation[1], orientation[0]]

def turn_right(orientation):
    # R270 = [[0,1],[-1,0]]
    return [orientation[1], -orientation[0]]

def at_cell(current_cell, other_cell):
    return current_cell[0] == other_cell[0] and current_cell[1] == other_cell[1]

# go to the right until you hit a wall
while not pixel_grid_at(update_cell(current_cell, orientation)):
    current_cell = update_cell(current_cell, orientation)
orientation = turn_left(orientation)

def front_free(current_cell, orientation):
    return not pixel_grid_at(update_cell(current_cell, orientation))

def will_have_right(current_cell, orientation):
    next_cell = update_cell(current_cell, orientation)
    next_right = update_cell(next_cell, turn_right(orientation))
    return pixel_grid_at(next_right)

plt.imshow(pixel_grid)
while not at_cell(current_cell, end_cell):
    ff = front_free(current_cell, orientation)
    whr = will_have_right(current_cell, orientation)
    if ff and whr:
        current_cell = update_cell(current_cell, orientation)
    if not ff:
        orientation = turn_left(orientation)
    if ff and not whr:
        current_cell = update_cell(current_cell, orientation)
        orientation = turn_right(orientation)
        current_cell = update_cell(current_cell, orientation)
    plt.scatter(current_cell[1], current_cell[0])
    if random.random() < 0.1:
        plt.pause(0.01)

plt.show()
