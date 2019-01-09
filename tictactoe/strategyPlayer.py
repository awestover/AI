# use the strategy json to make moves and play against a user

from whoWon import whoWon
import json
with open('strategy.json', 'r') as f:
    strategy = json.load(f)

def strReplace(s, i, new_chr):
    return s[:i]+new_chr + s[i+1:]

def displayBoard(state):
    readable = state.replace("E", "_")
    print(readable[:N]+"\n"+readable[N:2*N]+"\n"+readable[2*N:])

N = 3; M = 3
state = "EEEEEEEEE"
computerTurn = True
while whoWon(state, N, M) == "NoOne":
    if computerTurn:
        state = strategy[state]
        print("\n\nComputer Move")
        displayBoard(state)
        if whoWon(state, N, M) != "NoOne":
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
            
print("Game Over")
