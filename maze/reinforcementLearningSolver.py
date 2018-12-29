# The goal: find the optimal move from each state
# you can follow these to get to the end

# want the shortest path

# state space: each square on the grid (that is not a wall)
# valid transitions: up down left right
# value function: reward at the end. Penalize being in the maze for longer

import matplotlib.pyplot as plt
import json
with open('maze.json', 'r') as f:
    grid = json.load(f)
print(grid)
plt.imshow(grid)
plt.show()

states = [] # get everything that is not a wall
