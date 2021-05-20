from process.Aesmethod import Am_BZ, Am_S
from process.functions import createImage, newprogram,  programbreed, avgFitness,  trimarr, \
    population
from process.input import openfile
from PIL import Image

p1 = openfile("output/code9.cfdg")

# p2 = openfile("p2.cfdg")

'''''''''
arr = population(p1, p2, 10)
programbreed(arr, 10)

for i in range(len(arr)):
    createImage(str(arr[i]), "code" + str(i), "image" + str(i))
'''''''''
# print(Am_BZ(9, p1) * 1000)
# print(Am_S(9))


def bubbleSort(arr, d):
    n = len(arr)

    # 遍历所有数组元素
    for i in range(n):

        for j in range(0, n - i - 1):

            if d[arr[j]] < d[arr[j + 1]]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

d = [1,2,3,4,5]
arr = [1,2,3]
print(bubbleSort(arr, d))