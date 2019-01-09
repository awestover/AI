# AUTHOR: Alek Westover
# chopsticks solved with reinforcement learning

# NOTE: computer is X

# QUESTION: DO I need to reward ties?
# ANSWER: Probably...

N = 3 # grid size
M = 2 # number in a row for a win
import json

def strReplace(s, i, new_chr):
    return s[:i]+new_chr + s[i+1:]

wins = [
    "012", "345", "678", # horizontal
    "036", "147", "258", # vertical
    "048", "246" # cross
]

# this is really bad and not efficient and stuff!!!!!

# assumes that only 1 player wins in any state
# N by N tic tack toe grid, need to get M in a row
from whoWon import whoWon

# assumes that only 1 player wins in any state
def whoWonSimple(state):
    for win in wins:
        Xct = 0; Oct = 0
        for ws in win:
            if state[int(ws)] == "X":
                Xct += 1
            elif state[int(ws)] == "O":
                Oct += 1
        if Xct == 3:
            return "X"
        elif Oct == 3:
            return "O"
    for xi in state:
        if xi == "E":
            return "NoOne" # no one won yet
    return "Tie"  # it is a tie game

# generate the state space
# note: this includes some states where it is not Xs turn
# (which I will remove in states, because they are not actual states
# (i.e. the algorithm won't ever have to make a decision when it is Os turn))
states_by_depth = [set() for i in range(N*N+1)]
states_by_depth[0].add("E"*N*N)
for previous_depth in range(N*N):
    for previous_state in states_by_depth[previous_depth]:
        if whoWon(previous_state, N, M) == "NoOne":
            for idx in range(N*N):
                if previous_state[idx] == "E":
                    if previous_state.count("X") <= previous_state.count("O"):
                        states_by_depth[previous_depth+1].add(strReplace(previous_state, idx, "X"))
                    if previous_state.count("O") <= previous_state.count("X"):
                        states_by_depth[previous_depth+1].add(strReplace(previous_state, idx, "O"))

states = []
stateToIndex = {}
for depth in range(N*N+1):
    for state in states_by_depth[depth]:
        if state.count("O") >= state.count("X") or whoWon(state, N, M) != 'NoOne':
            states.append(state)
print(len(states))
for i in range(len(states)):
    stateToIndex[states[i]] = i
with open('ticTacToeStates.txt', 'w') as f:
    f.write("\n".join(states))

# COMPUTER is Xs, opponent is Os
transitions = []
"""
transitions
for each state in states:
    [{
        "action":
            if it is a non - end state: replace an E with an X somewhere,
            else: stay where you are
        "results":
            if computer just won
                [{
                    "nextState": yourself
                    "probability": 1
                    "reward": 1
                }]
            elif computer just tied
                [{
                    "nextState": yourself
                    "probability": 1
                    "reward": 0
                }]
            elif game was already over
                [{
                    "nextState": yourself
                    "probability": 1
                    "reward": 0
                }]
            else
            [
                {
                    "nextState":
                        "add an O somewhere",
                        "probability": random uniform opponent,
                        "reward":
                            if opponent wins: -1
                            else 0
                },
                {
                    "nextState":
                        something else
                }
            ]
"""
for state in states:
    actions = []
    if whoWon(state, N, M) == "NoOne":
        for idx in range(N*N):
            if state[idx] == "E":
                actions.append({"action": strReplace(state, idx, "X")})
    else:
        actions.append({"action": state})

    for action in actions:
        action["results"] = []
        if whoWon(state, N, M) == "NoOne" and whoWon(action["action"], N, M) == "X": # computer caused a win
            action["results"].append({
                "nextState": action["action"],
                "probability": 1,
                "reward": 1
            })
        elif whoWon(state, N, M) == "NoOne" and whoWon(action["action"], N, M) == "Tie": # computer caused a draw
            action["results"].append({
                "nextState": action["action"],
                "probability": 1,
                "reward": 0
            })
        elif whoWon(state, N, M) != "NoOne": # the game was already over
            action["results"].append({
                "nextState": action["action"],
                "probability": 1,
                "reward": 0
            })
        else:
            possible_next_states = []
            for idx in range(N*N):
                if action["action"][idx] == "E":
                    possible_next_states.append(strReplace(action["action"], idx, "O"))
            for next_state in possible_next_states:
                winner = whoWon(next_state, N, M)
                if winner == "O":
                    cur_reward = -1
                elif winner == "Tie":
                    cur_reward = -0.1
                else:
                    cur_reward = 0
                action["results"].append({
                    "nextState": next_state,
                    "probability": 1/len(possible_next_states),
                    "reward": cur_reward
                })
    transitions.append(actions)

values = [0 for i in range(len(states))]

# Bellman Equation
theta = 0.0001
delta = float('inf')
while delta > theta:
    delta = 0
    for i in range(len(states)):
        # new_value = max over actions of sum over outcomes given actions of probability * (reward + value)
        possible_new_values = []
        for action in transitions[i]:
            curTotalNewValue = 0
            for outcome in action['results']:
                curTotalNewValue += outcome['probability'] * (outcome['reward'] + values[stateToIndex[outcome['nextState']]])
            possible_new_values.append(curTotalNewValue)
        new_value = max(possible_new_values)
        tmpDelta = abs(values[i] - new_value)
        if tmpDelta > delta:
            delta = tmpDelta
        values[i] = new_value
    print(delta)

import matplotlib.pyplot as plt
plt.hist(values)
plt.show()

chosenActions = []
for i in range(len(states)):
    possible_values = []
    for action in transitions[i]:
        curTotalNewValue = 0
        for outcome in action['results']:
            curTotalNewValue += outcome['probability'] * (outcome['reward'] + values[stateToIndex[outcome['nextState']]])
        possible_values.append(curTotalNewValue)
    best_action = possible_values.index(max(possible_values))
    chosenActions.append(transitions[i][best_action]["action"])

strategyJson = {}
for i in range(len(states)):
    strategyJson[states[i]] = chosenActions[i]

with open('strategy.json', 'w') as f:
    json.dump(strategyJson, f)

import numpy as np
vv = np.array(values + [-1]*(81*81 - len(values)))
vv = vv.reshape((81, 81))
plt.imshow(vv)
plt.show()
