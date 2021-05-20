import cv2

from process.Kolmogorov import Kolmogorov
from process.entropy import get_entropy
from process.functions import createImage, newprogram, programreproduce, programbreed, avgFitness, fitness, trimarr, \
    population
from process.input import openfile
from PIL import Image


# Aesthetic measure BZ = Hp/K
def Am_BZ(filename):

    src = cv2.imread(filename + ".png")
    grayImage = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    Hp = get_entropy(grayImage)

    K = Kolmogorov(filename + ".cfdg")

    return Hp/K


# Aesthetic measure S = (Hp1+Hp2+Hp3+Hp4)/4Hp
def Am_S(filename):

    src = cv2.imread(filename + ".png")
    # 图像灰度化处理
    grayImage = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    shape = grayImage.shape
    w = shape[0]
    h = shape[1]

    # 对背景图进行上下分割 左上 右上 左下 右下
    pic1 = grayImage[0:int(w / 2), 0:int(h / 2)]
    pic2 = grayImage[0:int(w / 2), int(h / 2):h]
    pic3 = grayImage[int(w / 2):w, 0:int(h / 2)]
    pic4 = grayImage[int(w / 2):w, int(h / 2):h]

    Hp1 = get_entropy(pic1)
    Hp2 = get_entropy(pic2)
    Hp3 = get_entropy(pic3)
    Hp4 = get_entropy(pic4)
    Hp = get_entropy(grayImage)

    return (Hp1 + Hp2 + Hp3 + Hp4) / (4 * Hp)

