# recursive
def binarySearch(arr, val, i, j):
    if j - i < 1:
        return i
    mid = i + ((j-i)//2)
    if arr[mid] < val:
        return binarySearch(arr, val, mid + 1, j)
    elif arr[mid] > val:
        return binarySearch(arr, val, i, mid-1)
    else: # arr[mid] == val
        return mid

# not recursive
def binarySearchLoop(arr, val):
    i = 0; j = len(arr)-1
    while j - i >= 1:
        mid = i + ((j-i)//2)
        if arr[mid] < val:
            i = mid + 1
        elif arr[mid] > val:
            j = mid - 1
        else: # arr[mid] == val
            return mid
    return i
