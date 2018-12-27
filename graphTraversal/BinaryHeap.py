from Node import Node

# this is a min-heap (root is smallest element)
class BinaryHeap():
    def __init__(self):
        self.nodes = []
        self.length = 0

    def insert(self, node):
        # put it in at the bottom
        self.nodes.append(node)
        self.length += 1
        self.orderEnsuranceUp(self.length-1)

    # compare and swap with parent if it is smaller than the parent
    def orderEnsuranceUp(self, i):
        if i > 0:
            parentIdx = self.getParent(i)
            if self.nodes[i].getValue() < self.nodes[parentIdx].getValue():
                self.swap(i, parentIdx)
                self.orderEnsuranceUp(parentIdx)

    # compare and swap with smallest child if it is bigger than the child
    def orderEnsuranceDown(self, i):
        leftChildIdx = self.getLeftChild(i)
        rightChildIdx = leftChildIdx + 1
        if leftChildIdx < self.length:
            smallChildIdx = leftChildIdx
            if rightChildIdx < self.length:
                if self.nodes[rightChildIdx].getValue() < self.nodes[leftChildIdx].getValue():
                    smallChildIdx = rightChildIdx

            if self.nodes[smallChildIdx].getValue() < self.nodes[i].getValue():
                self.swap(smallChildIdx, i)
                self.orderEnsuranceDown(smallChildIdx)

    def deleteMin(self):
        self.nodes[0] = self.nodes[self.length - 1]
        self.length -= 1
        self.nodes.pop()
        self.orderEnsuranceDown(0)

    def swap(self, i, j):
        tmp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = tmp

    def findMin(self):
        return self.nodes[0]

    def getParent(self, idx):
        return (idx - 1)//2

    def getLeftChild(self, idx):
        return idx*2+1

    def isEmpty(self):
        return self.length == 0

    def __str__(self):
        return str(self.nodes)
