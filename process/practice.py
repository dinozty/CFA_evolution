from process.Aesmethod import Am_BZ, Am_S
from process.functions import createImage, newprogram, programbreed2, trimarr, \
    population, programbreed1, programbreed3, ms_fitness, make_file
from process.input import openfile
from PIL import Image

p1 = openfile("p1.cfdg")

p2 = openfile("p2.cfdg")

p3 = openfile("p3.cfdg")

p4 = openfile("p4.cfdg")

p5 = openfile("p5.cfdg")

p6 = openfile("p6.cfdg")


p7 = openfile("p7.cfdg")

p8 = openfile("p8.cfdg")

p9 = openfile("p9.cfdg")


pp = newprogram(p7, p3)
print(pp)



'''''''''
# 使用多目标优化
arr = population(p5, p6, 20) # 种群20 修改种群大小需要改部分代码
programbreed2(arr, 2)

'''''''''

'''''''''
# 使用交互式擂台赛
arr = population(p1, p2, 10) # 种群10 修改种群大小需要改部分代码
programbreed1(arr, 20)


'''''''''
'''''''''
# 使用单目标选择
arr = population(p2, p3, 20)
programbreed3(arr, 50)

'''''''''

'''''''''''
fit = [0.0] * 2
ms_fitness(p2)
ms_fitness(p3)
fit[0] = p2.getFit()
fit[1] = p3.getFit()
print(fit)
'''''''''