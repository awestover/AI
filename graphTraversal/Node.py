class Node:
    def __init__(self, index):
        self.index = index

    def getValue(self):
        return dists[self.index]

    def __str__(self):
        return "Distance: {}, totalDistanceEstimate: {}, index: {}".format(self.distance, self.totalDistanceEstimate, self.index)
