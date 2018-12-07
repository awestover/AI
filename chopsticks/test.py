# STATE CONVENTION
# [ your smaller hand, your bigger hand, opponent smaller hand, opponent bigger hand ]
# NOTE: this means I swap the hands every turn
# NOTE: there are thus (mod+1)*mod/2 = 15 for mod=5 possible hands in chopsticks
# NOTE: I expect that chopstick played optimally is allways a tie

import numpy as np
import pdb
import pprint

mod = 5 # maybe this could change later

# give a state a score
# 1 is win state
# -1 is lose state
# 0 otherwise
# note that [0,0,0,0] is scored as -1 although it doesn't matter since you can't reach this state
def scoreState(state):
    if state[0] == 0 and state[1] == 0:
        return -1
    elif state[2] == 0 and state[3] == 0:
        return 1
    else:
        return 0

# array state to string
def freezeState(state):
    return " ".join(map(str, state))

# string state to array
def unfreezeState(state):
    tmp = state.split(" ")
    return [int(ti) for ti in tmp]

# switch which hand is first
def swapHands(state):
    return state[2:] + state[:2]

def getValidMoves(state):
    moves = []

    # splits
    # take from small hand, give to big hand
    for j in range(1,state[0]):
        if(j+state[1]<mod):
            moves.append([state[0]-j, state[1]+j, state[2], state[3]])
    # take from big hand, give to small hand
    for j in range(1,state[1]):
        if(j+state[0]<mod and j+state[0] <= state[1]-j): # state[0] <= state[1] allways
            moves.append([state[0]+j, state[1]-j, state[2], state[3]])

    # hits
    # NOTE: THIS MIGHT BE WRONG, PLEASE CHECK IT: ARE THERE EVER DUPLICATES??????????????
    for i in range(0,2):
        if i == 0 and state[0] == state[1]: # don't double count if you have equal hands
            continue
        for j in range(2,4):
            if j == 2 and state[2] == state[3]: # don't double count if you have equal hands
                continue
            if state[i] != 0 and state[j] != 0:
                hit = (state[i] + state[j]) % mod
                nothit = state[(j-1)%2+2]
                moves.append([state[0], state[1], min(hit, nothit), max(hit,nothit)])

    return moves

# all valid hands
allValidHands = []
for i in range(0,mod):
    for j in range(0, i+1):
        allValidHands.append((j,i))
numValidHands = len(allValidHands)

# all valid states
stateToIndex = {}
indexToState = []
for i in range(numValidHands):
    for j in range(numValidHands):
        nextState = [allValidHands[i][0],allValidHands[i][1],allValidHands[j][0],allValidHands[j][1]]
        indexToState.append(nextState)
        stateToIndex[freezeState(nextState)] = numValidHands*i+j
numStates = len(indexToState)
transitionMatrix = np.zeros((numStates, numStates))

for i in range(numStates):
    nextMoves = getValidMoves(indexToState[i])
    # note the need 2 swap hands 2 times, it is allways the turn of whomevers hands are listed first!
    afterOpponentStates = [getValidMoves(swapHands(si)) for si in nextMoves]
    for j in range(len(afterOpponentStates)):
        for k in range(len(afterOpponentStates[j])):
            afterOpponentStates[j][k] = swapHands(afterOpponentStates[j][k])

    for path in afterOpponentStates:
        for opponentState in path:
            transitionMatrix[i][stateToIndex[freezeState(opponentState)]] = 1
            # NOTE: we are saying the matrix is:
            # |--to---
            # from
            # |
            # i.e. indexing by the state that we are at FIRST
            # this is significant because this is NOT what we did in math e23a

for i in range(numStates):
    print(indexToState[i], scoreState(indexToState[i]))
