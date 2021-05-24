from process.Aesmethod import Am_BZ, Am_S
from process.functions import createImage, newprogram, programbreed2, avgFitness, trimarr, \
    population, programbreed1
from process.input import openfile
from PIL import Image

p1 = openfile("p1.cfdg")

p2 = openfile("p2.cfdg")

'''''''''
# 使用多目标优化
arr = population(p1, p2, 20) # 种群20 修改种群大小需要改部分代码
programbreed2(arr, 10)

'''''''''


# 使用交互式擂台赛
arr = population(p1, p2, 10) # 种群10 修改种群大小需要改部分代码
programbreed1(arr, 10)



