
# get all the move combos
# assign probabilities
# play against the tree guy to train
# play against a human
"""
tic tac toe reinforcement learning

compute all game states, and transitions from them
initialize transition probabilities:
wins to 1
loses to 0
else to 0.5

play against an opponent:
chose either
with pr(eps)
random move

with pr(1-eps)
highest expected value move

evaluative learning

update transition probabilities
"""

from comboFuncs import *

# convention: I am player -1 (or player 2, just not player 1)

allBoards = [[]]
for pos in range(9):
    newBoards = []
    for val in [-1, 0, 1]:
        newBoards += [tboard + [val] for tboard in allBoards]
    allBoards = newBoards

boards = [] # only legit ones
for board in allBoards:
    if tookTurns(board, -1) and isEnd(board) == 0:
        boards.append(board)
print(len(boards))

nextBoards = []
scores = []
for board in boards:
    nextBoards.append(allPossibles(board, -1))
    scores.append([])
    for nb in nextBoards[-1]:
        res = isEnd(nb)
        if res == 1:
            scores[-1].append(0)
        elif res == -1:
            scores[-1].append(1)
        elif res == 2:
            scores[-1].append(0.75)
        else:
            scores[-1].append(0.5)

# print(nextBoards)
