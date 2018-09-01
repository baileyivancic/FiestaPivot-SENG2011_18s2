import sys
import copy

def isSubstring(token, string):
    i = 0
    r = False
    while (i < len(string) and  r == False):
        m = isPrefix(token, string[i:])
        if (m == True):
            r = True
        i +=1
    return r

def bubble(args):
    print("got in bubble")

    listCopy = copy.copy(args)
    i = (len(args) -1)
    upperbound = 0
    while (upperbound < len(args)):
        i = (len(args) - 1)
        while (i > upperbound):
            if (listCopy[i-1] > listCopy[i]):
                temp = listCopy[i]
                listCopy[i] = listCopy[i - 1]
                listCopy[i - 1] = temp
            i-= 1
        upperbound +=1
    return listCopy

def isPrefix(token, string):
    r = False
    if (len(token) == 0):
        r = True
    if (len(string) < len(token)):
        r = False
    else:
        r = (token == string[:len(token)])
    return r

temp = isSubstring(sys.argv[1], sys.argv[2])
if temp == True:
    print("yay")
else:
    print("no")