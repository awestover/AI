
arr = [0,1,2,3,4,5,6]

# flip 23 50
i = 2
j = 4
N = 7

ii = arr.index(i)
jj = arr.index(j)

minIdx = min(ii, jj)
maxIdx = max(ii, jj)
print(minIdx,maxIdx)
# reverse the subportion of the graph
for offIdx in range((maxIdx-minIdx)//2+1):
	tmp = arr[(minIdx+offIdx)%N]
	arr[(minIdx+offIdx)%N] = arr[(maxIdx-offIdx)%N]
	arr[(maxIdx-offIdx)%N] = tmp

print(arr)
