# use the strategy json to make moves and play against a user

import json
with open('strategy.json', 'r') as f:
    strategy = json.load(f)

def strReplace(s, i, new_chr):
    return s[:i]+new_chr + s[i+1:]

wins = [
    "012", "345", "678", # horizontal
    "036", "147", "258", # vertical
    "048", "246" # cross
]

# assumes that only 1 player wins in any state
def whoWon(state):
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

def displayBoard(state):
    readable = state.replace("E", "_")
    print(readable[:N]+"\n"+readable[N:2*N]+"\n"+readable[2*N:])

N = 3
state = "EEEEEEEEE"
computerTurn = False
while whoWon(state) == "NoOne":
    if computerTurn:
        state = strategy[state]
        print("\n\nComputer Move")
        displayBoard(state)
        if whoWon(state) != "NoOne":
            break
        computerTurn = False
    else:
        move = input("\n\nWhat is your move?\t")
        try:
            move = int(move)
            if move >= N*N:
                continue
            if state[move] != "E":
                continue
            state = strReplace(state, move, "O")
            print("\n\nPlayer Move")
            displayBoard(state)
            computerTurn = True
        except:
            continue
