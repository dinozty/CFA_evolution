
# classes.py: contains all class definitions for program
import random


class Program:  # has startshape, which shapeDef, and a dictionary of nodes
    def __str__(self):
        return """
startshape {startshape}
CF::MinimumSize = 0.3
CF::MaxShapes = 100000

{shapes}
		""".format(startshape=self.startshape.name, shapes="\n".join(str(k) for k in self.shapes))

    def __lt__(self, other):  # override <操作符
        if self.fitness == other.fitness:
            return random.choice([1, -1])
        return self.fitness > other.fitness

    def __init__(self, startshape, shapes):  # 输入str 保存为dictionary
        self.fitness = 1.0
        self.rank = 1 # 默认存活
        self.shapes = shapes  # 字典格式
        self.startshape = self.findNT(startshape)
        if self.startshape == None:
            print("shape ", startshape, "not found in NonTerminals")

    def findNT(self, name):
        for c in self.shapes:
            if (c.name == name):
                return c
        return None

    def addShape(self, shape):
        self.shapes[shape.name] = shape

    def setFit(self, fitness):
        self.fitness = fitness

    def getFit(self):
        return self.fitness

    def setRank(self, rank):
        self.rank = rank

    def getRank(self):
        return self.rank

class NonTerminal:
    def __str__(self):
        return ("shape " + self.name + "\n" + "\n".join(str(k) for k in self.children))

    def __init__(self, name, children, program=None):
        self.children = list(children)
        self.name = name
        for c in self.children:
            c.parent = self
        self.program = program

    def setProgram(self, p):
        self.program = p

    def addShapeDef(self, shapedef):
        self.children.append(shapedef)
        shapedef.parent = self

    def __copy__(self):
        return self.copyHelper({})

    def copyHelper(self, dictionary):
        if self in dictionary:
            return dictionary[self]
        else:
            clist = []
            result = NonTerminal(self.name, [])
            dictionary[self] = result
            for c in self.children:
                result.addShapeDef(c.copyHelper(dictionary))
            return result


class ShapeDef:
    def __str__(self):
        return "rule " + str(self.weight) + "{\n" + "\n".join(str(x) for x in self.children) + " \n } \n"

    def __init__(self, parent, children, weight=1):
        self.parent = parent
        self.children = children
        self.weight = weight

    def __copy__(self):
        return self.copyHelper({})

    def copyHelper(self, dictionary):
        if self in dictionary:
            return dictionary[self]
        else:
            cList = []
            result = ShapeDef(None, cList, self.weight)
            dictionary[self] = result
            for c in self.children:
                cList.append(c.copyHelper(dictionary))
            return result


class Node:
    def __str__(self):
        return "unimplemented"

    def __init__(self, children):
        self.children = children

    def __copy__(self):
        return self.copyHelper({})

    def copyHelper(self, dictionary):
        if self in dictionary:
            return dictionary[self]
        else:
            cList = []
            result = type(self)(cList)
            dictionary[self] = result
            for c in self.children:
                cList.append(c.copyHelper(dictionary))
            return result


class Shape(Node):
    def __str__(self):
        return "{} [{}]".format(self.name, self.argsStr())

    def __init__(self, name, args):
        super().__init__(args)
        self.name = name

    def argsStr(self):
        return " ".join(str(c) for c in self.children)


class SimpleShape(Shape):
    def __init__(self, args):
        super().__init__(None, args)
        del self.name


class RuleCall(Shape):
    def __init__(self, rule, args):
        if (rule == None):
            super().__init__("__noName__", args)
        else:
            super().__init__(rule.name, args)
        self.rule = rule

    def __str__(self):
        self.name = self.rule.name
        return super().__str__()

    def setRule(self, rule):
        self.rule = rule
        self.name = rule.name

    def __copy__(self):
        return self.copyHelper({})

    def copyHelper(self, dictionary):
        if self in dictionary:
            return dictionary[self]
        else:
            cList = []
            result = type(self)(None, cList)
            dictionary[self] = result
            toPrint = self.rule.copyHelper(dictionary)
            result.setRule(toPrint)
            for c in self.children:
                cList.append(c.copyHelper(dictionary))

            return result


# shapes
class Square(SimpleShape):
    name = "SQUARE"


class Circle(SimpleShape):
    name = "CIRCLE"


class Triangle(SimpleShape):
    name = "TRIANGLE"


class Modifier:
    def __str__(self):
        return "{} {}".format(self.name, " ".join(str(v) for v in self.values))

    def __init__(self, *values):
        self.values = values

    def __copy__(self):
        return self.copyHelper({})

    def copyHelper(self, dictionary):
        if self in dictionary:
            return dictionary[self]
        else:
            return type(self)(*self.values)


# modifers and value
# 1
class Alpha(Modifier):
    name = "a"


# 1
class Brightness(Modifier):
    name = "b"


# 1
class Saturation(Modifier):
    name = "sat"


# 1
class Hue(Modifier):
    name = "h"


# 1
class Y(Modifier):
    name = "y"


# 1
class Z(Modifier):
    name = "z"


# 1
class Rotate(Modifier):
    name = "r"


# 1
class Flip(Modifier):
    name = "f"


# 1, 2, 3
class X(Modifier):
    name = "x"


# 1, 2, 3
class Size(Modifier):  # if this larger than certain number, does not work well
    name = "s"


# takes 1, 2, 4, 6
class Transform(Modifier):
    name = "trans"


# takes 2
class Skew(Modifier):
    name = "skew"


# takes 1
class randRange(Modifier):
    name = ".."


class Leftbrac(Modifier):
    name = "["


class Rightbrac(Modifier):
    name = "]"


class Value:
    def __str__(self):
        return repr(self.val)

    def __init__(self, val):
        self.val = val




