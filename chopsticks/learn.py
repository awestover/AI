# AUTOR: Alek Westover
# chopsticks reinforcement learning

# STATE CONVENTION
# [ your smaller hand, your bigger hand, opponent smaller hand, opponent bigger hand ]
# NOTE: this means I swap the hands every turn
# NOTE: there are thus (mod+1)*mod/2 = 15 for mod=5 possible hands in chopsticks
# NOTE: I expect that chopstick played optimally is allways a tie

import numpy as np
from utilityFunctions import *
import matplotlib.pyplot as plt
import json

mod = 5 # could change later

# all valid hands
allValidHands = []
for i in range(0,mod):
    for j in range(0, i+1):
        allValidHands.append((j,i))
numValidHands = len(allValidHands)

# all valid states
allStates = []
stateToIndex = {}
for i in range(numValidHands):
    for j in range(numValidHands):
        nextState = [allValidHands[i][0],allValidHands[i][1],allValidHands[j][0],allValidHands[j][1]]
        allStates.append(nextState)
        stateToIndex[freezeState(nextState)] = i*numValidHands+j
numStates = len(allStates)
transitions = []
def storeidx(state):
    return stateToIndex[freezeState(state)]

# for example:
# transitions[storeidx([0, 1, 0, 1]] = [{"newState": storeidx([0, 1, 0, 2]), "reward":scoreState([0,1,0,2]), "nextStates": [storeidx([0,1,1,1]),storeidx([0,3,0,2])], "prs": [1]}]

for i in range(numStates):
    transitions.append([])
    nextMoves = validNextStates(allStates[i], mod) # NOTE: i = storeidx(allStates[i])
    for nextMove in nextMoves:
        # NOTE: need to swap hands 2 times, it is allways the turn of whomevers hands are listed first!
        reward = scoreState(nextMove)
        if scoreState(allStates[i]) != 0:
            reward = 0
        nextStates = [storeidx(swapHands(si)) for si in validNextStates(swapHands(nextMove), mod)]
        transitions[i].append({"reward": reward, "newState": storeidx(nextMove), "nextStates": nextStates, "prs": [1.0/len(nextStates) for si in nextStates]})

values = [scoreState(state)*0 for state in allStates]
# values = [2*(np.random.random()-0.5) for state in allStates]

gamma = 1#0.999999
theta = 0.0000001 # 0.0001
converged = False
itter = 0
while not converged:
    delta = 0
    itter += 1
    print(itter)
    for i in range(numStates):
        oldValue = values[i]
        valuesForActions = []
        for action in transitions[i]:
            valueAction = 0
            for j in range(len(action["nextStates"])):
                valueAction += action["prs"][j]*(action["reward"]+gamma*values[action["nextStates"][j]])
            valuesForActions.append(valueAction)
        values[i] = max(valuesForActions)
        delta = max(delta, abs(oldValue-values[i]))
    if delta < theta:
        converged = True
    else:
        vvTemp = np.array(values).reshape(numValidHands, numValidHands)
        plt.imshow(vvTemp)
        plt.pause(0.1)
plt.show()

with open("results.json", 'w') as f:
    json.dump({
                "gamma": gamma, "mod":mod,
                "allStates":allStates, "values":values,
                "transitions":transitions, "stateToIndex": stateToIndex
                }, f)

# lots of the values are really close to 1, but not quite 1, and they are distinguishable
#plt.hist(values)
#plt.show()

#def superZoom(x, y):
#    return (x**(-y)) / -y


#def superZoomPlot(y):
#    plt.hist(superZoom(0.0000000001+1-np.array(values), y))
#    plt.show()

#import pdb; pdb.set_trace()
#superZoomPlot(18)

#large_values = [vi for vi in values if vi > 0.999]

#print(min(large_values))
#print(max(large_values))
