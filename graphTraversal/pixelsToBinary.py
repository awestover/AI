import json
import numpy as np
from PIL import Image
# img = Image.open('smallMaze.png')
img = Image.open('actualMaze.png')
arr = np.array(img)[:,:,:3]

walls = np.zeros((arr.shape[0], arr.shape[1]))
# walls are black

black = np.array([0,0,0])
white = np.array([255,255,255])
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        if np.linalg.norm(black - arr[i][j]) > np.linalg.norm(white - arr[i][j]):
            walls[i,j] = False
        else:
            walls[i,j] = True
walls = walls.tolist()

import matplotlib.pyplot as plt
plt.imshow(walls)
plt.show()

with open('smallMaze.json', 'w') as f:
    json.dump(walls, f)
