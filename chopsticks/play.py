# AUTOR: Alek Westover
# chopsticks player

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

print("Mod {}".format(mod))
print("computer allways listed first FYI")
state = storeidx([1,1,1,1])
while scoreState(allStates[state]) == 0:
    # computer move
    state = chooseMove(state)
    print("Computer went, state is:")
    print(allStates[state])
    # player move, unless computer won
    if scoreState(allStates[state]) == 0:
        validMove = False
        while not validMove:
            move = input("please input a move like this: h11 h12 h21 h22\n").split(" ")
            if len(move) == 4:
                try:
                    move = [int(mi)%mod for mi in move]
                except:
                    continue
                if move[0] > move[1]:
                    move[1], move[0] = move[0], move[1]
                if move[2] > move[3]:
                    move[2], move[3] = move[3], move[2]
                possibleMoves = getValidMoves(swapHands(allStates[state]), mod)
                possibleMoves = [storeidx(swapHands(pm)) for pm in possibleMoves]
                if storeidx(move) in possibleMoves:
                    validMove = True
        state = storeidx(move)
        print("Player went, state is:")
        print(allStates[state])

print("game over")
