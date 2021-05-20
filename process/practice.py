from process.functions import createImage, newprogram, programreproduce, programbreed, avgFitness, fitness, trimarr
from process.input import openfile
from PIL import Image

p1 = openfile("p1.txt")

p2 = openfile("p2.txt")

programarr = [p1, p2]


'''''''''''
# 进化代数 100 交互次数 1，10，20，30，40，50，60，70，80，90
manselect = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89]
for i in range(10):

    programreproduce(programarr)             # pick parents here
    # currently only doing one generation, can increase second param to however many generations wanted
    programarr = trimarr(programarr)
    if i in manselect:
        print(len(programarr))
        for j in range(len(programarr)):
            # createImage(str(programarr[j]), ("code" + str(i) + " " + str(j)), ("result" + str(i) + " " + str(j)))
            # img = Image.open("output/" + "result" + str(i) + " " + str(j) + ".png")
            # img.show()
            fit = float(input("该图片的评分为:"))
            # img.close()
            programarr[j].setFit(fit)

for j in range(len(programarr)):
    createImage(str(programarr[j]), ("code" + str(i) + " " + str(j)), ("result" + str(i) + " " + str(j)))
    # img = Image.open("output/" + "result" + str(i) + " " + str(j) + ".png")
    # img.show()


'''''''''