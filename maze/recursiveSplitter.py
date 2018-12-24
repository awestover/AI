
import matplotlib.pyplot as plt
import random

# note that this is not quite working: a wall can block off a previous hole in a wall
# I can't think of a great way to fix this besides having the hole indices determine where the walls are, which seems
# about as complicated as my below comment (see end of the file)

# make walls on the portion of the grid from start i (si) to end i (ei) (both endpoints included)
def wallDivide(si, ei, sj, ej):
    # base case of the recursion is to do nothing, happens if the grid is too small
    # make walls
    print(si,ei,sj,ej)
    if random.random() < 0.1:
        plt.imshow(grid); plt.pause(0.1)
    if ei - si >= 2 and ej - sj >= 2:
        wallJ = random.randint(sj+1,ej-1)
        for i in range(si, ei+1):
            grid[i][wallJ] = 1

        wallI = random.randint(si+1,ei-1)
        for j in range(sj, ej+1):
            grid[wallI][j] = 1
        # put holes in walls
        holeLeft = random.randint(sj,wallJ-1)
        holeRight = random.randint(wallJ+1,ej)
        grid[wallI][holeLeft] = 0
        grid[wallI][holeRight] = 0
        holeDown = random.randint(wallI+1,ei)
        grid[holeDown][wallJ] = 0
        # divide each of the 4 new regions
        wallDivide(si, wallI-1, sj, wallJ-1)
        wallDivide(wallI+1, ei, sj, wallJ-1)
        wallDivide(si, wallI-1, wallJ+1, ej)
        wallDivide(wallI+1, ei, wallJ+1, ej)

N = 10
# 0 means no wall, 1 means there is a wall
grid = [[0 for j in range(N)] for i in range(N)]
wallDivide(0, N-1, 0, N-1)
plt.imshow(grid)
plt.show()


# I know there is a better way than this
# what if the recursive method also took in a start and end location as arguments
# then it could make it so that you had to travel through all 4 quadrants every time...
# but it still wouldn't be a GREAT maze, so I probably won't bother, especially since I think I would have to hard code in 2* (4 choose 2) = 12 cases for this...
