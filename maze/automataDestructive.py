
import random

N = 100
grid = [[0 if random.random()<0.5 else 1 for j in range(N)] for i in range(N)]

def neighbor_update_rule(neighbor_ct, current_state):
    if 1 <= neighbor_ct <= 5 and current_state:
        return 1
    else:
        return 0

def update(grid):
    change_ct = 0
    new_grid = [[0 for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            neighbor_ct = 0
            for ii in [-1, 0, 1]:
                for jj in [-1, 0, 1]:
                    if ii != 0 or jj != 0:
                        if i + ii >= 0 and i + ii <= N-1:
                            if j + jj >= 0 and j + jj <= N-1:
                                if grid[i+ii][j+jj]:
                                    neighbor_ct += 1
            tmp = grid[i][j]
            new_grid[i][j] = neighbor_update_rule(neighbor_ct, grid[i][j])
            if tmp != new_grid[i][j]:
                change_ct += 1
    return new_grid, change_ct

num_changed = N*N
import matplotlib.pyplot as plt
i = 0
while num_changed > 0 and i < 1000:
    plt.imshow(grid)
    plt.show()
    grid, num_changed = update(grid)
    i += 1
print(i)
plt.imshow(grid)
plt.show()
