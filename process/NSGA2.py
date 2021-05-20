

# NSGA-II 算法

import numpy as np

maxn = 0xffffffff

# 快速非支配排序算法
def fast_non_dominated_sort(fitness, num):
    P = num
    S = [[] for i in range(num)]
    n = [0] * num
    rank = [0] * num
    F = [[] for i in range(num)]
    returnF = []
    for p in range(P):

        for q in range(P):
            if fitness[p][0] >= fitness[q][0] and fitness[p][1] >= fitness[q][1]:  # p支配q
                S[p].append(q)
                # print(S[q])
            elif fitness[p][0] <= fitness[q][0] and fitness[p][1] <= fitness[q][1]:  # p被q所支配
                n[p] = n[p] + 1
                # print(n[p])
        if n[p] == 0:
            rank[p] = 0
            F[0].append(p)

    i = 0
    while F[i]:
        Q = []
        for p in F[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if n[q] == 0:
                    rank[q] = i + 1
                    Q.append(q)
        if not Q:
            break
        i = i + 1
        F[i] = Q

    for i in range(num):
        if F[i]:
            returnF.append(F[i])

    return returnF, rank


# 快速排序：按照fit[arr[i]]排序，从小到大

def quickSort(arr, fit, left=None, right=None):
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

# 拥挤度函数

def crowding_distance_assignment(fitness, num, F):
    i = 0
    distance = [0.0] * num
    l = len(F)
    for i in range(l): # 每一阶层
        T = F[i]

        for r in range(2):
            fit = np.array(fitness)[:, r]  # 按照第一列和第二列排序
            # print(fit)
            T = quickSort(T, fit)  # 从小到大排序
            # print(T)
            lt = len(T) - 1
            distance[T[0]] = distance[T[lt]] = maxn
            for s in range(1, lt-1):
                distance[T[s]] = distance[T[s]] + (fit[T[s + 1]] - fit[T[s - 1]])

    return distance



'''''''''
fitness = [[0, 4], [1, 3], [2, 2], [3, 1]]
F, rank = fast_non_dominated_sort(fitness, 4)
dis = crowding_distance_assignment(fitness, 4, F)

print(dis)

'''''''''

