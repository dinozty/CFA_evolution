# 压缩代码来自：https://github.com/bytemo/Blog/tree/master/Huffman

# -*- coding: utf-8 -*-
import sys


# 数据初始化

node_dict = {}  # 建立原始数据与编码节点的映射，便于稍后输出数据的编码
count_dict = {}
ec_dict = {}
nodes = []
inverse_dict = {}


# 定义哈夫曼树的节点类
class node(object):

    def __init__(self, value=None, left=None, right=None, father=None):
        self.value = value
        self.left = left
        self.right = right
        self.father = father

    def build_father(left, right):
        n = node(value=left.value + right.value, left=left, right=right)
        left.father = right.father = n
        return n

    def encode(n):
        if n.father == None:
            return b''
        if n.father.left == n:
            return node.encode(n.father) + b'0'  # 左节点编号'0'
        else:
            return node.encode(n.father) + b'1'  # 右节点编号'1'


# 哈夫曼树构建
def build_tree(l):
    if len(l) == 1:
        return l
    sorts = sorted(l, key=lambda x: x.value, reverse=False)
    n = node.build_father(sorts[0], sorts[1])
    sorts.pop(0)
    sorts.pop(0)
    sorts.append(n)
    return build_tree(sorts)


def encode(echo):
    for x in node_dict.keys():
        ec_dict[x] = node.encode(node_dict[x])


# 压缩操作
def encodefile(inputfile):

    f = open(inputfile, "rb")
    bytes_width = 1  # 每次读取的字节宽度
    i = 0

    f.seek(0, 2)
    count = f.tell() / bytes_width
    # print(count)
    nodes = []  # 结点列表，用于构建哈夫曼树
    buff = [b''] * int(count)
    f.seek(0)

    # 计算字符频率,并将单个字符构建成单一节点
    while i < count:
        buff[i] = f.read(bytes_width)
        if count_dict.get(buff[i], -1) == -1:
            count_dict[buff[i]] = 0
        count_dict[buff[i]] = count_dict[buff[i]] + 1
        i = i + 1


    for x in count_dict.keys():
        node_dict[x] = node(count_dict[x])
        nodes.append(node_dict[x])

    f.close()
    tree = build_tree(nodes)  # 哈夫曼树构建
    encode(False)  # 构建编码表


    head = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)  # 对所有根节点进行排序
    bit_width = 1


    if head[0][1] > 255:
        bit_width = 2
        if head[0][1] > 65535:
            bit_width = 3
            if head[0][1] > 16777215:
                bit_width = 4

    i = 0
    raw = 0b1
    last = 0

    condense = []

    while i < count:  # 开始压缩数据
        for x in ec_dict[buff[i]]:
            raw = raw << 1
            if x == 49:
                raw = raw | 1
            if raw.bit_length() == 9:
                raw = raw & (~(1 << 8))
                condense.append(int.to_bytes(raw, 1, byteorder='big'))
                raw = 0b1
                tem = int(i / len(buff) * 100)
                if tem > last:
                    last = tem
        i = i + 1

    if raw.bit_length() > 1:  # 处理文件尾部不足一个字节的数据
        raw = raw << (8 - (raw.bit_length() - 1))
        raw = raw & (~(1 << raw.bit_length() - 1))
        condense.append(int.to_bytes(raw, 1, byteorder='big'))
    return len(condense)


# 用压缩后的二进制文件长度来代表程序的柯氏复杂度
def Kolmogorov(file):

    return encodefile(file)

