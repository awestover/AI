# 2x2 Rubik's Cube Solver
# Authors: Alek and Max
# https://www.youcandothecube.com/solve-it/2-x-2-solution

import numpy as np
from pprint import pprint

cube = []

COLORS = ['G', 'Y', 'B', 'W', 'O', 'R']

for color in COLORS:
    cube.append(np.array([[color, color],[color, color]]))

# indpairs specifies what side goes to what side
# ind flips is the indices on those sides to flip
# ie for R turn the first column of 1 into the first column of 0
"""
   [0]
[5][1][4]
   [2]
   [3]
"""
moves = {
    "R":  {"indpairs":[(1,0),(2,1),(3,2),(0,3)], "indflips":([0,1],1)},
    "Ri": {"indpairs":[(0,1),(1,2),(2,3),(3,0)], "indflips":([0,1],1)},
    "U":  {"indpairs":[(0,4),(5,0),(2,5),(4,2)], "indflips":(0)},
    "Ui": {"indpairs":[(4,0),(0,5),(5,2),(2,4)], "indflips":(0)},
    "L":  {"indpairs":[(0,1),(1,2),(2,3),(3,0)], "indflips":([0,1],0)},
    "Li": {"indpairs":[(1,0),(2,1),(3,2),(0,3)], "indflips":([0,1],0)}
}

algs = {}
algs["Fish_1"] = ['R','U','Ri','U','R','U','U','Ri']
algs["Fish_2"] = algs["Fish_1"]+['U']+['U']+algs["Fish_1"]
algs["The_Cat(Website case 5)"] = algs["Fish_1"]+['U']+algs["Fish_2"]
algs["Diagonal(Website case 7)"] = algs["Fish_1"]+algs["Fish_2"]
algs["The_double_sides(Website case 2)"] = algs["Fish_1"]+algs["Fish_1"]
algs["(Website case 3)"] = algs["Fish_1"]+['U']+algs["Fish_1"]
algs["(Webiste case 6)"] = algs["Fish_1"]+['Ui']+["Fish_2"]

# "state name": [([faceIndex, [indexOnFace]], "COLOR", True/False (should it be this color or not this color)), other requirements]
states = {
    "Fish_1": [([1, [1,0]], "Y", True)]
}
tmp = []
for i in range(len(COLORS)):
    tmp.append(([i, [0, 0]], COLORS[i], True))
    tmp.append(([i, [0, 1]], COLORS[i], True))
    tmp.append(([i, [1, 0]], COLORS[i], True))
    tmp.append(([i, [1, 1]], COLORS[i], True))
states["solved"] = tmp
states['whiteFace'] = [([0, [0,0]], "W", False), etc]

stateOrder = ["solved", "whiteFace", "Fish_1"]

def rotate(oldcube, move):
    newcube = [np.copy(oldcubei) for oldcubei in oldcube]
    for indpair in moves[move]["indpairs"]:
        newcube[indpair[1]][moves[move]["indflips"]] = oldcube[indpair[0]][moves[move]["indflips"]]
    return newcube

def doFormula(oldcube, formula):
    for move in formula:
        oldcube = rotate(oldcube, move)
    return oldcube

def isState(cube, state):
    for req in state:
        if (cube[req[0][0]][req[0][1][0], req[0][1][1]] == req[1]) == req[2]:
            return False
    return True

def getState(cube):
    for state in stateOrder:
        try:
            if isState(cube, states[state]):
                return state
        except KeyError:
            print("not done yet")
            continue
    return "none"

cube = rotate(cube, 'R')
pprint(cube)
while True:
    state = getState(cube)
    print(state)

    if state == "solved":
        print("The computer solved your cube. Now go solve it yourself")
        break
    elif state == "Fish_1":
        cube = doFormula(cube, algs['Fish_1'])
        break
    else:
        print("I don't know how to do this yet")
        break

pprint(cube)
