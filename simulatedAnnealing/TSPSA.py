
"""
arr: array to opperate on
i, j: start, end index of subArray
N: total legth of array
"""
def flipSubArr(arr, i, j, N):
	minIdx = min(i, j)
	maxIdx = max(i, j)
	# reverse the subportion of the graph
	for offIdx in range((maxIdx-minIdx)//2+1):
		tmp = arr[(minIdx+offIdx)%N]
		arr[(minIdx+offIdx)%N] = arr[(maxIdx-offIdx)%N]
		arr[(maxIdx-offIdx)%N] = tmp

# display a state (set of vertices)
def displayState(X, verts, pause=True):
	plt.plot(X[verts+[verts[0]],0],X[verts+[verts[0]],1])
	if pause:
		plt.pause(0.5)
		plt.cla()
	else:
		plt.show()

# calculate the value of a state
def value(X, verts, N):
	val = 0
	for v in range(N):
		val += np.linalg.norm(X[verts[v]]-X[verts[(v+1)%N]])
	return val

# calculate the change in value caused by changing a pair of edges
def dValue(X, verts, i, j, N):
	# before: i -> i-1, j -> j+1
	# now: i -> j+1, j -> i-1
	initValue = np.linalg.norm(X[verts[i]]-X[verts[(i-1)%N]]) + np.linalg.norm(X[verts[j]]-X[verts[(j+1)%N]])
	finalValue = np.linalg.norm(X[verts[i]]-X[verts[(j+1)%N]]) + np.linalg.norm(X[verts[j]]-X[verts[(i-1)%N]])
	return finalValue - initValue

# get indices i,j for a swap 
def randomSwap(N):
	i = np.random.randint(N)
	j = (i+2+np.random.randint(N-3)) % N

	return min(i,j),max(i,j)

# generate the data
import numpy as np
import matplotlib.pyplot as plt
N = 100
X = np.random.random((N,2))

Tcur = np.sqrt(2)
# Tmax = 10000; Tmin = 10
# def temperature(Temp): # need to experiment with this some more
	# return Temp*0.00001
	# return (Temp**0.5)*0.288/5000

verts = [i for i in range(N)]
curValue = value(X, verts, N)

badMovesTaken = []
values = []

gamma = 0.99

for i in range(100000):
# for Temp in range(Tmax, Tmin,-1):
	# if Temp % 1000 == 0:
		# displayState(X, verts, pause=False)
	Tcur = Tcur*gamma

	proposedSwap = randomSwap(N)
	# test = verts[:]
	# flipSubArr(test, *proposedSwap, N)
	# dVal = value(X, test, N) - value(X, verts, N)
	dVal = dValue(X, verts, *proposedSwap, N)

	# dVal < 0 -> it is a good move, exploit it 
	# else -> not a good move, may explore anyways in case it leads to a good move
	if dVal < 0 or np.exp(-dVal / Tcur) > np.random.random(): 
		flipSubArr(verts, *proposedSwap, N)
		curValue += dVal
		values.append(dVal)
		if dVal > 0:
			badMovesTaken.append(1)
		else:
			badMovesTaken.append(0)

badMoveIdxs = [i for i in range(len(badMovesTaken)) if badMovesTaken[i]==1]
plt.hist(badMoveIdxs)
plt.show()

plt.plot(values)
plt.show()

displayState(X, verts, pause=False)
