# AUTOR: Alek Westover
# chopsticks Utility Functions

import numpy as np

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

def getValidMoves(state, mod):
    if scoreState(state) != 0: # terminal states lead to themselves ONLY AND ALLWAYS
        return [state]

    moves = []
    # splits
    # take from small hand, give to big hand
    for j in range(1,state[0]+1):
        if(j+state[1]<mod):
            moves.append([state[0]-j, state[1]+j, state[2], state[3]])
    # take from big hand, give to small hand
    for j in range(1,state[1]+1):
        if(j+state[0]<mod and j+state[0] <= state[1]-j): # state[0] <= state[1] allways
            moves.append([state[0]+j, state[1]-j, state[2], state[3]])

    # hits
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
