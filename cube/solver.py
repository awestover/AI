# 2x2 Rubik's Cube Solver
# Authors: Alek and Max
# https://www.youcandothecube.com/solve-it/2-x-2-solution

import numpy as np
from pprint import pprint
import requests

cube = []
COLORS = ['G', 'Y', 'B', 'W', 'R', 'O']
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

On all faces this is what it looks like in terms of indices
[00 01]
[10 11]


"""
moves = {
    "R":  {"indpairs":[(1,0),(2,1),(3,2),(0,3)], "indflips":([0,1],1)},
    "Ri": {"indpairs":[(0,1),(1,2),(2,3),(3,0)], "indflips":([0,1],1)},
    "U":  {"indpairs":[(0,4),(5,0),(2,5),(4,2)], "indflips":(0)},
    "Ui": {"indpairs":[(4,0),(0,5),(5,2),(2,4)], "indflips":(0)},
    "L":  {"indpairs":[(0,1),(1,2),(2,3),(3,0)], "indflips":([0,1],0)},
    "Li": {"indpairs":[(1,0),(2,1),(3,2),(0,3)], "indflips":([0,1],0)},
    "F":  {"indpairs":[(1,4),(4,3),(3,5),(5,1)], "indflips":(1)},
    "Fi": {"indpairs":[(4,1),(3,4),(5,3),(1,5)], "indflips":(1)},
    "B":  {"indpairs":[(4,1),(3,4),(5,3),(1,5)], "indflips":(0)},
    "Bi": {"indpairs":[(1,4),(4,3),(3,5),(5,1)], "indflips":(0)},
    "D":  {"indpairs":[(4,0),(0,5),(5,2),(2,4)], "indflips":(1)},
    "Di": {"indpairs":[(0,4),(5,0),(2,5),(4,2)], "indflips":(1)}
}

algs = {}
algs["Fish_1"] = ['R','U','Ri','U','R','U','U','Ri']
algs["Fish_2"] = algs["Fish_1"]+['U']+['U']+algs["Fish_1"]
algs["The_Cat(Website case 5)"] = algs["Fish_1"]+['U']+algs["Fish_2"]
algs["Diagonal(Website case 7)"] = algs["Fish_1"]+algs["Fish_2"]
algs["The_double_sides(Website case 2)"] = algs["Fish_1"]+algs["Fish_1"]
algs["(Website case 3)"] = algs["Fish_1"]+['U']+algs["Fish_1"]
algs["(Webiste case 6)"] = algs["Fish_1"]+['Ui']+["Fish_2"]
algs["Diagonal PLL"] = ['Ri','F','Ri','B','B','R','Fi','Ri','B','B','R','R']
algs["Parralel PLL switch"] = algs["Diagonal PLL"]+['Ui']

algs['upRotation'] =   ['R', 'Li']
algs['sideRotation'] = ['U', 'Di']
algs['frontRotation'] = ['F', 'Bi']

# requirements for state. Format:
# "state name": [([faceIndex, [indexOnFace]], "COLOR", True/False (should it be this color?)), other_requierments]
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
states['whiteFace'] = [([3, [0,0]], "W", True),([3, [0,1]], "W", True),([3, [1,0]], "W", True),
    ([3, [1,1]], "W", True),([0, [1,0]], "G", True),([0, [1,1]], "G", True),
    ([2, [1,0]], "B", True),([2, [1,1]], "B", True),([4, [1,0]], "O", True),
    ([4, [1,1]], "O", True),([5, [1,0]], "R", True),([5, [1,1]], "R", True)]
states['yellowFace'] = [([1, [0,0]], "Y", True), ([1, [0,1]], "Y", True), 
                        ([1, [1,0]], "Y", True), ([1, [1,1]], "Y", True)]

yellowSolveAlgs = ['Fish_1']
pllSolveAlgs = ['Diagonal PLL', 'Parralel PLL switch']

def rotate(oldcube, move):
    newcube = [np.copy(oldcubei) for oldcubei in oldcube]
    for indpair in moves[move]["indpairs"]:
        newcube[indpair[1]][moves[move]["indflips"]] = oldcube[indpair[0]][moves[move]["indflips"]]
    return newcube

def doFormula(oldcube, formula):
    for move in formula:
        oldcube = rotate(oldcube, move)
    return oldcube

def findCorner(oldcube, colors):
    acorner = [(0, [0,1]),(1,[1,1]),(4,[1,0])]
    boolCube = [np.array([[False, False], [False, False]]) for i in range(6)]
    
    


def solveWhite(oldcube):
    if not(oldcube[3][1,0] == 'W' and oldcube[0][1,1] == 'G' and oldcube[5][1,0] == 'O'):
        while 
    return oldcube

def isState(cube, state):
    for req in state:
        if (cube[req[0][0]][req[0][1][0], req[0][1][1]] == req[1]) == req[2]:
            return False
    return True

cube = rotate(cube, 'U')
pprint(cube)
while True:
    if isState(cube, states['solved']):
        print('The computer solved your cube. Now go solve the cube yourself :P')
        break
    else:
        if not isState(cube, states['whiteFace']):
            solveWhite(cube)
            print('I don\'t know how to solve the white face yet...')
            break
        else:
            if not isState(cube, states['yellowFace']):
                print("fish etc")
                didSomething = False
                for state in yellowSolveAlgs:
                    if isState(cube, states[state]):
                        doFormula(cube, algs[state])
                        didSomething = True
                if not didSomething:
                    # do Up rotation
                    print('This yellow state is too hard to solve (AKA I am not programmed for it correctly)')
                    break
            else:
                print('PLL')
                didSomething = False
                for state in pllSolveAlgs:
                    if isState(cube, states[state]):
                        doFormula(cube, algs[state])
                        didSomething = True
                if not didSomething:
                    print('PLL didn\'t happen, but it probably should have')
                    break
def sendData():
    tmp = []
    for a in cube:
        tmp.append(a.tolist())
    requests.post("http://127.0.0.1:5000/cubeData", json={"cubeData":tmp})


pprint(cube)
try:
    sendData()
except:
    print('web thing is not running')
