
import json

with open("strategy5.json", 'r') as f:
    data = json.load(f)
allStates = data['allStates']
strategy = data['strategy']

def game(start, debug=False):
    state = start
    ct = 0
    while ct < 1000 and not ((allStates[state][0]+allStates[state][1] == 0) or (allStates[state][2]+allStates[state][3]==0)):
        if debug:
            print(allStates[state])
        state = strategy[str(state)]
        ct += 1
    if allStates[state][0]+allStates[state][1] == 0:
        return 0
    elif allStates[state][2] + allStates[state][3] == 0:
        return 1
    else:
        return -1

for i in range(len(allStates)):
    print(i, allStates[i], game(i))
# game(32, debug=True)