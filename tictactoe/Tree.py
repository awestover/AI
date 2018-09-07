class Tree:
    def __init__(self, state, val=0):
        self.state = state
        self.val = val
        self.childs = []

    def score(self, goal=1):
        if self.val != 0:
            return self.val

        tiePosible = False
        for child in self.childs:
            if child.score(goal=-goal) == goal:
                self.val = goal
                return goal
            elif child.val == 2:
                tiePosible = True

        if tiePosible:  # a tie is better than a loss
            self.val = 2
            return 2

        # if you can't win or tie you lose
        self.val = -goal
        return -goal

    def __str__(self):
        return str(self.state)

    def pp(self, t=0):
        print("\t"*t + ''.join([str(xi) for xi in self.state]))
        for child in self.childs:
            child.pp(t=t+1)

    def pvs(self, t=0, tcap=9):
        if t < tcap:
            if self.val != 0:
                print("\t"*t + str(self.val), self.state)
                for child in self.childs:
                    child.pvs(t=t+1, tcap=tcap)

    def pv(self, t=0, tcap=9, goal=1):
        if t < tcap:
            if self.val != 0:
                print("\t"*t + "{} ({})".format(self.val, str(goal)))
                for child in self.childs:
                    child.pv(t=t+1, tcap=tcap, goal=-goal)
