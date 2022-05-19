import sys
import random

class Pointer:
    x = 0
    y = 0
    dir = 0
    
    def next(self):
        if self.dir == 0:
            self.x += 1
        if self.dir == 1:
            self.y += 1
        if self.dir == 2:
            self.x -= 1
        if self.dir == 3:
            self.y -= 1

stack = []
plane = []
ptr = Pointer()

instruction_table = {
    "0" : "pushNumber(0)",
    "1" : "pushNumber(1)",
    "2" : "pushNumber(2)",
    "3" : "pushNumber(3)",
    "4" : "pushNumber(4)",
    "5" : "pushNumber(5)",
    "6" : "pushNumber(6)",
    "7" : "pushNumber(7)",
    "8" : "pushNumber(8)",
    "9" : "pushNumber(9)",
    "+" : "add()",
    "-" : "subtract()",
    "*" : "multiply()",
    "/" : "intDivision()",
    "%" : "modulo()",
    "!" : "logicalNot()",
    "`" : "compare()",
    ">" : "changeDir(0)",
    "v" : "changeDir(1)",
    "<" : "changeDir(2)",
    "^" : "changeDir(3)",
    "?" : "randomDirection()",
    "_" : "ifHorizontal()",
    "|" : "ifVertical()",
    '"' : "wordInterpreter()",
    ":" : "duplicateValueOnStack()",
    "\\" : "swapTwoStackElements()",
    "$" : "discardPop()",
    "." : "popAndOutput()",
    "," : "outputASCII()",
    "#" : "skipNext()",
    "p" : "putCall()",
    "g" : "getCall()",
    "@" : "doNothing()", #implemented in while loop as exit condition
    " " : "doNothing()"
}

#instruction implementations
#############################################################
# [0-9]
def pushNumber(num):
    stack.append(num)

# +
def add():
    a = stack.pop()
    b = stack.pop()
    stack.append(a+b)

# -
def subtract():
    a = stack.pop()
    b = stack.pop()
    stack.append(b-a)
    
# *
def multiply():
    a = stack.pop()
    b = stack.pop()
    stack.append(a*b)    

# /
def intDivision():
    a = stack.pop()
    b = stack.pop()
    stack.append(int(b/a))
    
# %
def modulo():
    a = stack.pop()
    b = stack.pop()
    if a == 0:
        stack.append(0)
    else:
        stack.append(b%a)

# !
def logicalNot():
    val = stack.pop()
    if val == 0:
        stack.append(1)
    else:
        stack.append(0)

# `
def compare():
    a = stack.pop()
    b = stack.pop()
    if b>a:
        stack.append(1)
    else:
        stack.append(0)
    
# < v > ^
def changeDir(dir):
    ptr.dir = dir
    
# ?
def randomDirection():
    ptr.dir = random.randint(0,3)

# _
def ifHorizontal():
    num = stack.pop()
    if num == 0:
        ptr.dir = 0
        return
    ptr.dir = 2
    
# |
def ifVertical():
    num = stack.pop()
    if num == 0:
        ptr.dir = 1
        return
    ptr.dir = 3
    
# "
def wordInterpreter():
    ptr.next()
    instruction = ""
    while True:
        instruction = plane[ptr.y][ptr.x]
        if instruction == '"':
            break;
        stack.append(ord(instruction))
        ptr.next()
         
# :
def duplicateValueOnStack():
    if len(stack) == 0:
        stack.append(0)
        return
    num = stack.pop()
    stack.append(num)
    stack.append(num)

# \
def swapTwoStackElements():
    if len(stack) == 1:
        stack.append(0)
        return
    else:
        e1 = stack.pop()
        e2 = stack.pop()
        stack.append(e1)
        stack.append(e2)
        return
    
    
# $
def discardPop():
    stack.pop()
    
# . 
def popAndOutput():
    return str(stack.pop()) + " "

# ,
def outputASCII():
    return chr(stack.pop())
# #
def skipNext():
    ptr.next()

# p
def putCall():
    y = stack.pop()
    x = stack.pop()
    v = stack.pop()
    plane[y][x] = chr(v)
    
# g
def getCall():
    y = stack.pop()
    x = stack.pop()
    stack.append(ord(plane[y][x]))
    
# whitespace
def doNothing():
    return
    

#############################################################

def interpret(code):
    global ptr
    global stack
    output = ""
    createPlane(code)
    instruction = ""
    ptr = Pointer()
    stack = []
    iter = 0
    #interpretation loop
    while instruction != "@":
        instruction = plane[ptr.y][ptr.x]
        try:
            out = eval(instruction_table[instruction])
            if out is not None:
                output += out
        except:
            print("invalid function call: " + instruction)
        ptr.next()
        iter += 1
    return output

def createPlane(code):
    global plane
    splitted = code.split("\n")
    elements = [list(p) for p in splitted]
    plane = [["" for i in range(80)] for u in range(25)]
    for i in range(len(elements)):
        for u in range(len(elements[i])):
            plane[i][u] = elements[i][u]

if len(sys.argv) == 2:
    filepath = sys.argv[1]
    print("Interpreting: " + filepath)
    seperator = ""
    if sys.platform == "linux" or sys.platform == "linux2":
        seperator = "/"
    elif sys.platform == "win32":
        seperator = "\\"
    filename = sys.argv[1].split("\\")
    fileending = filename[len(filename)-1].split(".")
    if fileending[1] == "befunge":
        file = open(filepath,"r")
        code = file.read()
        print(interpret(code))
    else:
        print("File must have the .befugne ending!")

else:
    print("Usage: python BefungeInterpreter.py [Filename].befunge")

