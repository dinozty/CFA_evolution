import numpy as np

from process.Aesmethod import Am_BZ, Am_S
from process.input import openfile


def quickSort(arr, fit, left=None, right=None): # 按照fit[arr[i]]排序，从小到大
    left = 0 if not isinstance(left,(int, float)) else left
    right = len(arr)-1 if not isinstance(right,(int, float)) else right
    if left < right:
        partitionIndex = partition(arr, fit, left, right)
        quickSort(arr, fit, left, partitionIndex-1)
        quickSort(arr, fit, partitionIndex+1, right)
    return arr

def partition(arr, fit, left, right):
    pivot = left
    index = pivot+1
    i = index
    while  i <= right:
        if fit[arr[i]] < fit[arr[pivot]]:
            swap(arr, i, index)
            index += 1
        i += 1
    swap(arr, pivot, index-1)
    return index-1

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

fit = [5,4,3,2,1]
arr = [0,1,2,3,4]
fitt = [[0,4],[1,3],[2,2],[3,1],[4,0]]

# f = np.array(fitt)[:,1]
# print(f)
# print(quickSort(arr, f))

F = [[],[1,2],[]]


print(len(F))