# The goal: find the optimal move from each state
# you can follow these to get to the end

# want the shortest path

# state space: each square on the grid (that is not a wall)
# valid transitions: up down left right
# value function: reward at the end. Penalize being in the maze for longer

import matplotlib.pyplot as plt
import json
with open('maze.json', 'r') as f:
    walls = json.load(f)
N = len(walls)
# plt.imshow(walls)
# plt.show()

def wallIdxToArrIdx(i, j):
    return N*i+j

def arrIdxToWallIdx(k):
    return (k//N, k%N)

# states are "state 0" which means whatever grid square is stored in index 0 of the states array (stored as a number which is an index into an array representing the maze)
states = [] # get everything that is not a wall
indexesToStates = {}
for i in range(N):
    for j in range(N):
        if not walls[i][j]:
            states.append(wallIdxToArrIdx(i, j))
for i in range(len(states)):
    indexesToStates[states[i]] = i
end_state = len(states)-1

transitions = [] # a list of possible moves from each state (up down left right (unless you are an "edge" (literaly) case))

def transition_reward(state, new_state):
    if state == end_state:
        return 0 # only should get rewarded once for winning
    else:
        if new_state == end_state:
            return 0
        else:
            return -1

for i in range(len(states)):
    transitions.append([])
    curIndex = arrIdxToWallIdx(states[i])
    if i == end_state:
        transitions[-1].append({"new_state": end_state, "probability": 1, "reward": transition_reward(i, end_state)})
    else:
        new_indexes = []
        if curIndex[0] > 0 and not walls[curIndex[0]-1][curIndex[1]]:
            new_indexes.append(wallIdxToArrIdx(curIndex[0]-1, curIndex[1]))
        if curIndex[1] > 0 and not walls[curIndex[0]][curIndex[1]-1]:
            new_indexes.append(wallIdxToArrIdx(curIndex[0], curIndex[1]-1))
        if curIndex[0] < N-1 and not walls[curIndex[0]+1][curIndex[1]]:
            new_indexes.append(wallIdxToArrIdx(curIndex[0]+1, curIndex[1]))
        if curIndex[1] < N-1 and not walls[curIndex[0]][curIndex[1]+1]:
            new_indexes.append(wallIdxToArrIdx(curIndex[0], curIndex[1]+1))
        for new_idx in new_indexes:
            new_state = indexesToStates[new_idx]
            transitions[-1].append({"new_state": new_state, "probability": 1, "reward": transition_reward(i, new_state)})

values = [0 for i in range(len(states))]

delta = float('inf')
theta = 0.01
while delta > theta:
    delta = 0
    for i in range(len(states)):
        possible_next_values = []
        for action in transitions[i]:
            # NOTE: there is only 1 possible new state, happens with probability 1
            possible_next_values.append(action["reward"] + values[action["new_state"]])
        new_value = max(possible_next_values)
        if abs(new_value - values[i]) > delta:
            delta = abs(new_value - values[i])
        values[i] = new_value
    print(delta)

plt.gca().invert_yaxis()
valueGrid = [[min(values)+10 for j in range(N)] for i in range(N)]
for i in range(len(states)):
    curIdx = arrIdxToWallIdx(states[i])
    valueGrid[curIdx[0]][curIdx[1]] = values[i]
plt.imshow(valueGrid)
plt.show()

index = 0
sequence = []
while index != end_state:
    move_expected_values = []
    for action in transitions[index]:
        move_expected_values.append(action["reward"] + values[action["new_state"]])
    move = transitions[index][move_expected_values.index(max(move_expected_values))]
    index = move["new_state"]
    sequence.append(arrIdxToWallIdx(states[index]))
    print(index, end_state)

plt.gca().invert_yaxis()
plt.imshow(valueGrid)
for i in range(len(sequence)-1):
    plt.plot([sequence[i][1], sequence[i+1][1]], [sequence[i][0], sequence[i+1][0]], c='b')
plt.show()

plt.imshow(walls)
for i in range(len(sequence)-1):
    plt.plot([sequence[i][1], sequence[i+1][1]], [sequence[i][0], sequence[i+1][0]], c='b')
plt.show()
