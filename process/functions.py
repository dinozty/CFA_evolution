# functions.py: contains all functions to be used for generating new programs

# imports
import math
import random

import subprocess
import os
import copy
import string
import classes
from classes import Triangle, Square, Circle, Skew, Alpha, Brightness, Saturation, Hue, Y, Z, Rotate, Flip, X, \
    Transform, ShapeDef, NonTerminal, Shape, Program, RuleCall, Modifier, SimpleShape




def pickPartner(rule, p1, p2):  # 随机选取交叉对象shapedef
    parent = rule.parent.program
    otherParent = (p1, p2)[parent == p1]  # 属于另一个程序

    ran = random.choice(otherParent.shapes) # 另一个程序中的nt集合 随机取一个nt

    return random.choice(ran.children) # 返回另一个程序中的随机一个shapedef


def slicechildren(children, numparts):  # 生成numparts长度的列表，每个元素放入[shapedef]，方便交叉

    toReturn = [None] * numparts
    size = int(math.ceil(len(children) / numparts))
    splitAt = [0]
    for i in range(numparts):

        splitAt.append(splitAt[-1] + size)

    for i in range(numparts):

        toReturn[i] = children[splitAt[i]: splitAt[i + 1]]

    return toReturn


# increase or decrease by a percent - not always good for multiple generations
def mutateParamVal(param):

    param = float(param)
    ran = random.uniform(0, 99)
    if ran > 90:
        return param * 1.001
    if ran < 10:
        return param * 0.999
    else:
        return param


def mutateSimpleShape(shape):

    ran = random.uniform(0, 99)

    if ran > 1:
        nshape = random.choice([Square(shape.children), Circle(shape.children), Triangle(shape.children)])
        if nshape.name == shape.name:
            return mutateSimpleShape(shape)
        return nshape

    else:
        return shape




# 交叉： 随机选择双亲nt的shapedef进行组合 返回一连串shapedef
def crossSequences(s1, s2):
    splits = [3, 4, 5, 8, 34]
    numparts = random.choice(splits)

    p1arr = slicechildren(s1, numparts)
    p2arr = slicechildren(s2, numparts)

    attributes = []
    for i in range(0, numparts):
        ran = random.uniform(0, 99)

        if (ran < 50):
            attributes.extend(p1arr[i])

        else:
            attributes.extend(p2arr[i])

    return attributes




def mutation(crosschildren,kind): # 发生变异

    # print(crosschildren)
    if kind == 1: # 变异方式：参数变化
        for c in range(len(crosschildren)):
            newChildren = []
            for p in crosschildren[c].children: # 具体的shape
                newValues = []
                for val in p.values: # p：一个参数类
                    newValues.append(mutateParamVal(val))  # param mutation
                p.values = newValues
                newChildren.extend([p])
                crosschildren[c].children = newChildren

    if kind == 2: # 变异方式：简单图形随机变形
        newshape = []
        for p in crosschildren:
            if not isinstance(p, SimpleShape):
                newshape.append(p)
            else:
                print(p)
                newshape.append(mutateSimpleShape(p))
        crosschildren = newshape

    return crosschildren


# 对shapedef进行交叉，交换shape（simpleshape & rulecall）
def crossShapeDef(rule, partner, p1, p2):  # add extra rule - more complexity

    crosschildren = crossSequences(rule.children, partner.children) # 元素是shapedef的列表

    # call cross attributes

    weight = random.choice([rule.weight, partner.weight]) # 出现概率
    lenVar = len(crosschildren) # 选取后的shapedef个数

    if lenVar == 0:     # 重新选取
        return crossShapeDef(rule, partner, p1, p2)

    # 发生变异
    crosschildren = mutation(crosschildren, 1)
    crosschildren = mutation(crosschildren, 2)

    return ShapeDef(None, crosschildren, weight)



# 检测并添加引用但没有包含的图形定义
def flattenNT(nt, soFar=None):
    if soFar == None:
        soFar = {nt} # 元素不重复 集合

    result = [nt]

    for rule in nt.children:
        for shape in rule.children:
            if isinstance(shape, RuleCall) and shape not in result:
                if shape.rule not in soFar: # 引用的rule未被加入定义
                    soFar.add(shape.rule)
                    result.extend(flattenNT(shape.rule, soFar))
    return result



# 对nt进行交叉
def crossNT(nt1, nt2, p1, p2):

    rules = crossSequences(nt1.children, nt2.children) # 实际上只对startshape中的内容进行交叉

    result = [] # 新nt中所有rule集合

    for rule in rules:
        partner = pickPartner(rule, p1, p2)  # a shapedef
        newShapeDef = crossShapeDef(rule, partner, p1, p2)
        result.append(newShapeDef)

    ran = random.uniform(0, 99)

    # 50%的几率添加新rule定义
    if ran > 50:
        rule = random.choice(rules)
        partner = pickPartner(rule, p1, p2)  # a shapedef
        newShapeDef = crossShapeDef(rule, partner, p1, p2)
        result.append(newShapeDef)

        name = nt1.name
    else:
        name = nt2.name

    returnNT = NonTerminal(name, result)
    return flattenNT(returnNT)


# crossover for programs - doesn't take care of shape parameters
# will need to iterate if more than one shape
def newprogram(p1, p2):

    result = crossNT(p1.startshape, p2.startshape, p1, p2) # 返回一堆nt [{}]
    return Program(result[0].name, result)



def Tournament(arr, p1, p2):

    # check = int(input("请您挑出更好的一张：前者（1）or后者（2）"))
    check = 1  # 暂时测试
    if check == 1:
        return [p1, p2]
    return [p2, p1]

# 随机从其他优胜者中挑选另一个亲本
def select_p2(arr, x):

    p = random.randint(0, len(arr)-1)
    if not p == x:
        return p
    return select_p2(arr, x)


# result = [win_id, lose_id]
# 交互式锦标赛选择法
# 每一轮随机选择两者进行对抗，胜者拥有繁衍权，败者淘汰，胜者组互相繁衍补充空位
def Tournament_Selection(arr):
    length = len(arr)
    childarr = []
    parentarr = []
    random.shuffle(arr)
    for x in range(int(length/2)):
        opp = length-x-1
        result = Tournament(arr, x, opp)
        arr[result[0]].setRank(1)  # 存活
        arr[result[1]].setRank(0)  # 去世

    for i in range(length):
        if arr[i].rank == 1:
            parentarr.append(arr[i])

    for i in range(len(arr)):

        p2 = select_p2(arr, i)
        newp = newprogram(arr[i], arr[p2])
        childarr.append(newp)

    return parentarr + childarr



#
def programreproduce(arr):

    trr = []
    trr.append(arr[0])
    trr.append(arr[1])
    for i in range(8):
        child = newprogram(arr[0], arr[1])
        trr.append(child)
    arr.clear()
    arr = trr



# 适应度值 自动
def fitness(program):
    # new fitness:

    # want to determine the size of the program
    # num = len(program.shapes)
    # sum = 0
    # total = 0
    # for i in range (num):
    # 	children = program.shapes[i].children   #shapedefs
    # 	for j in range(len(children)):
    # 		sum += len(program.shapes[i].children[j].children) # children of a shapedef: shapes: rules or simpleshapes
    # 		total += 1

    # avg = sum/total
    # return avg  # number of things within rule

    # old fitness:
    return len(program.shapes)  # num nonterminals


# 按照适应度以及一点点运气排序

# 保留适应度前十的图形
def trimarr(programarr):
    programarr.sort()
    return programarr[0:10]


#


#  获取平均适应度
def avgFitness(parr):
    total = 0
    num = len(parr)
    for i in range(num):
        total += parr[i].getFit()

    return total / num


# 获取初代种群
def population(p1, p2, large):

    arr = []
    for i in range(large):
        arr.append(newprogram(p1, p2))
    return arr



# 进行迭代
def programbreed(programarr, num): # 列表 范围 迭代数

        for i in range(num):
            programarr = Tournament_Selection(programarr)



# 产生文件和图像
def createImage(code, codeName, resultName):
    if (not os.path.exists("output")):
        os.mkdir("output")

    with open("output/" + codeName + ".cfdg", "w") as fout:
        fout.write(code)


    subprocess.run(["../ContextFree/ContextFreeCLI.exe", "output/" + codeName + ".cfdg", "output/" + resultName + ".png"])

