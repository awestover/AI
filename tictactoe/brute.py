# convention: player 1 and player -1
# board is filled with 0s initially and then 1, -1 alternate
# a game state is scored -1 if it is a lose state, 1 if it is a win state,
# 0 if we don't know yet, and 2 if it is a tie

from Tree import Tree
from comboFuncs import isEnd, allPossibles

def getTurn(state, first=1):
    if state.count(first) > state.count(-first):
        return -first
    else:
        return first

def getMove(state):
    root = Tree(state)
    leafs = [root]
    goal = getTurn(state, first=1) # first=which player (-1/+1) went first
    for i in range(9+1):
        print("Depth i={}".format(i))
        new_leafs = []
        for leaf in leafs:
            possibles = allPossibles(leaf.state, goal*((-1)**i))
            if len(possibles) == 0:
                leaf.val = isEnd(leaf.state)
            else:
                for possible in possibles:
                    new_leafs.append(Tree(possible, 0))
                    leaf.childs.append(new_leafs[-1])
        print("number of leaves = {}".format(len(leafs)))
        leafs = new_leafs

    root.score()
    print("\nFound scores")
    root.pv(tcap=3, goal=goal)
    bestMove = -1
    outcome = 'lose'
    for i in range(len(root.childs)):
        if root.childs[i].val == 2 and bestMove == -1:
            bestMove = i
            outcome = 'tie'
        elif root.childs[i].val == 1:
            bestMove = i
            outcome = 'win'
            break
    print("If you do this move: ")
    print(root.childs[i].state)
    print("And both players play optimally")
    print("You will {}".format(outcome))

if __name__ == "__main__":
    getMove([0]*9)
    # getMove([1,1,-1, 0,-1,0, 0,0,0])
    # getMove([1,0,0, 0,-1,0, 0,0,0])
