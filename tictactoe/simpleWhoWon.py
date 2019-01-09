
# this only works for 3 by 3 tic tac toe with 3 in a row
wins = [
    "012", "345", "678", # horizontal
    "036", "147", "258", # vertical
    "048", "246" # cross
]


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
