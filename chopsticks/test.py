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
def scoreState(state):
    if state[0] == 0 and state[1] == 0:
        return -1
    elif state[2] == 0 and state[3] == 0:
        return 1
    else:
        return 0

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

print(getValidMoves([0,4,1,2]))
