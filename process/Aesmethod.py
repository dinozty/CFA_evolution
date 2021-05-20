import cv2

from process.Kolmogorov import Kolmogorov
from process.entropy import get_entropy



# Aesthetic measure BZ = Hp/K high：形状更复杂代码更简洁
def Am_BZ(num, p):

    src = cv2.imread("output/image" + str(num) + ".png")
    grayImage = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    Hp = get_entropy(grayImage)
    # print(Hp)

    K = Kolmogorov(p)
    # print(K)

    return (Hp/K) * 1000 # 归一化处理？


# Aesthetic measure S = (Hp1+Hp2+Hp3+Hp4)/4Hp high：形状更均匀
def Am_S(num):

    src = cv2.imread("output/image" + str(num) + ".png")
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

