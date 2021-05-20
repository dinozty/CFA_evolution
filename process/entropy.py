import math

import cv2
import numpy as np


# 得到图片的审美措施S的值
def get_AMS(pic_add):

    src = cv2.imread(pic_add)
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

    '''''''''
    cv2.imshow("pic1", pic1)
    cv2.imshow("pic2", pic2)
    cv2.imshow("pic3", pic3)
    cv2.imshow("pic4", pic4)
    '''''''''

    Hp1 = get_entropy(pic1)
    Hp2 = get_entropy(pic2)
    Hp3 = get_entropy(pic3)
    Hp4 = get_entropy(pic4)
    Hp = get_entropy(grayImage)

    # S = (Hp1+Hp2+Hp3+Hp4)/4Hp
    return (Hp1 + Hp2 + Hp3 + Hp4) / (4 * Hp)


# 计算灰度图的信息熵
def get_entropy(image):
    tmp = []
    for i in range(256):
        tmp.append(0)
    k = 0
    res = 0.0
    img = np.array(image)
    for i in range(len(img)):
        for j in range(len(img[i])):
            val = img[i][j]
            tmp[val] = float(tmp[val] + 1)
            k = float(k + 1)
    for i in range(len(tmp)):
        tmp[i] = float(tmp[i] / k)
    for i in range(len(tmp)):
        if (tmp[i] == 0):
            res = res
        else:
            res = float(res - tmp[i] * (math.log(tmp[i]) / math.log(2.0)))
    return res


# print(get_AMS("output/image9.png"))
