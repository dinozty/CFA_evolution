from process.functions import createImage, newprogram, programreproduce, programbreed, avgFitness, fitness, trimarr, \
    population
from process.input import openfile
from PIL import Image

p1 = openfile("p1.txt")

p2 = openfile("p2.txt")

'''''''''
arr = population(p1, p2, 10)
programbreed(arr, 10)



for i in range(len(arr)):
    createImage(str(arr[i]), ("code" + str(i)), ("image" + str(i)))

'''''''''

string = str(p2)

text = string.strip().replace(' ', '').replace('\n', '').replace('\r', '')

print(text)