# makes an easier to use strategy json

import json
from utilityFunctions import *

with open('results.json', 'r') as f:
    data = json.load(f)

allStates = data["allStates"]
transitions = data["transitions"]
values = data["values"]
gamma = data["gamma"]
stateToIndex = data["stateToIndex"]
mod = data["mod"]

def storeidx(state):
    return stateToIndex[freezeState(state)]

def chooseMove(stateIdx):
    valuesForActions = []
    for action in transitions[stateIdx]:
        valueAction = 0
        for j in range(len(action["nextStates"])):
            valueAction += action["prs"][j]*(action["reward"]+gamma*values[action["nextStates"][j]])
        valuesForActions.append(valueAction)
    return transitions[stateIdx][np.argmax(valuesForActions)]['newState']

# write out strategy in easy to understand form
strategy = {"allStates": allStates, "strategy": {}}
for state in allStates:
    strategy["strategy"][storeidx(state)] = chooseMove(storeidx(state))

with open("strategy{}.json".format(mod), 'w') as f:
    json.dump(strategy, f)
