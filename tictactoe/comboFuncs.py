wins = [
    "012", "345", "678", # horizontal
    "036", "147", "258", # vertical
    "048", "246" # cross
]

# assumes that only 1 player wins in any state
def isEnd(state):
    for win in wins:
        ct = 0
        for ws in win:
            ct += state[int(ws)]
        if ct == 3:
            return 1
        elif ct == -3:
            return -1
    for xi in state:
        if xi == 0:
            return 0
    # if the whole board is full and no one won it is a tie
    return 2

# checks to see if there are multiple wins (by player 1 and 2, not double wins)
# no LEGIT state has this return True
def multipleWins(state):
    p1Wins = False; p2Wins = False;
    for win in wins:
        ct = 0
        for ws in win:
            ct += state[int(ws)]
        if ct == 3:
            p1Wins = True
        elif ct == -3:
            p2Wins = True
    return p1Wins and p2Wins


# are the number of player pieces roughly equitable (+/-1), turn is +/- 1
def tookTurns(state, turn):
    res = state.count(-turn) - state.count(turn)
    return res == 0 or res == 1

# takes in the state as a vector and the turn as a number (+1 or -1)
def allPossibles(state, turn):
    if isEnd(state) != 0:
        return []
    moves = []
    for idx in range(9):
        if state[idx] == 0:
            tmp = state[:]
            tmp[idx] = turn
            moves.append(tmp)
    return moves
