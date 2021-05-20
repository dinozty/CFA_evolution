import re

from classes import Triangle, Size, Square, Circle, Skew, Alpha, Brightness, Saturation, Hue, Y, Rotate, Flip, X, \
    Transform, ShapeDef, NonTerminal, Program, RuleCall, randRange, Leftbrac, Rightbrac


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False

def atomconvert(text,nts):
    parr = [] # eg.[a 1 b 2 ]
    atomparr = [] # eg.[1 2 3]
    parr.clear()
    atomparr.clear()

    sumflag = 0
    for chip in reversed(text):
        # print(chip)
        if "]" in chip:
            sumflag = sumflag + chip.count("]")
            # print(sumflag)
        chip = chip.replace("[", "")
        chip = chip.replace("]", "")
        # print(chip)

        if is_number(chip): # 如果是数字

            atomparr.append(float(chip))

        else:                   # 如果是字母
            list.reverse(atomparr)

            if chip == "a" or chip == "alpha":
                parr.append(Alpha(*atomparr))

            elif chip == "b" or chip == "brightness":
                parr.append(Brightness(*atomparr))

            elif chip == "sat" or chip == "saturation":
                parr.append(Saturation(*atomparr))

            elif chip == "h" or chip == "hue":
                parr.append(Hue(*atomparr))

            elif chip == "y":
                parr.append(Y(*atomparr))

            elif chip == "r" or chip == "rotate":
                parr.append(Rotate(*atomparr))

            elif chip == "f" or chip == "flip":
                parr.append(Flip(*atomparr))

            elif chip == "x":
                parr.append(X(*atomparr))

            elif chip == "s" or chip == "size":
                parr.append(Size(*atomparr))

            elif chip == "trans" or chip == "transform":
                parr.append(Transform(*atomparr))

            elif chip == "skew":
                parr.append(Skew(*atomparr))

            elif chip == "..":
                parr.append(randRange(*atomparr))


            # 统计完毕一个参数，清空数字列表
            atomparr.clear()


    list.reverse(parr)

    if sumflag == 2:
        # print("GG")
        parr = [Leftbrac()] + parr + [Rightbrac()]

    if text[0] == "CIRCLE":
        return Circle(parr)

    elif text[0] == "TRIANGLE":
        return Triangle(parr)

    elif text[0] == "SQUARE":
        return Square(parr)

    else:
        ntName = text[0]
        for n in nts:
            if ntName == n.name:
                return RuleCall(n, parr)

        newNT = NonTerminal(ntName, [])
        nts.append(newNT)
        return RuleCall(newNT,parr)


Simshapes = ["CIRCLE", "SQUARE", "TRIANGLE"]

 # 所有nt,一个程序中有一个


def openfile(file):

    nts = []
    nts.clear()

    with open(file, "r") as f:  # 打开文件
        f = f.readlines()
        # opens = f[0].split()
        flag = 0
        atomshapes = []  # rule xx{}
        shapes = []  # shape xx {} 所有rules，一个nt中有一个
        atomshapes.clear()
        shapes.clear()

        for line in reversed(f):

            line.strip()
            # print(line) #

            if not line.find("}") == -1:
                flag = 1
               # print("1 ",flag) #

                atomshapes.clear()

            elif not line.find("{") == -1 and flag == 1:
                flag = 0
                # print("2 ",flag) #

            line = line.replace("{", "") # 这一行
            text = line.split()  # 切片列表

            if flag == 1: # 读入状态

                if len(text) > 1:
                    # print("3 ", flag)  #
                    '''''''''
                    if text[0] in Simshapes:  ## 若为简单图形
                        atomshapes.append(atomconvert(text))
                    else: ## 若为自定义图形
                        atomshapes.append(rullconvert(text,nts))
                    '''''''''
                    atomshapes.append(atomconvert(text, nts)) ## 统一处理
            else: #   装配阶段

                if not line.find("shape") == -1:

                    ll = line.split()
                    fflag = 0

                    if not shapes: # 如果省略了rule
                        shapes.append(ShapeDef(None, list(reversed(atomshapes[:]))))

                    # rule中内容已装
                    for nt in nts:
                        if nt.name == ll[1]: # nt已存在与列表中

                            for s in reversed(shapes): ##
                                nt.addShapeDef(s)
                            # nt.addShapeDef(shapes[:])
                            fflag = 1

                    if fflag == 0: # 新建nt
                        nts.append(NonTerminal(ll[1], shapes[:]))

                    shapes.clear()

                elif not line.find("rule") == -1:  # 装入rule中

                    if len(text) == 1:
                        shapes.append(ShapeDef(None, list(reversed(atomshapes[:]))))
                    elif len(text) == 2:
                        shapes.append(ShapeDef(None, list(reversed(atomshapes[:])), float(text[1])))


        # print("ok")
        # print(f[0].split()[1])
        list.reverse(nts)

    p = Program(f[0].split()[1], nts)
    return p







