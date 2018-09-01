# Written by Bailey Ivancic - converted from Dafny verified code written by Harry Tang and Nabil Shaikh
import sys
import copy


def bubble(args):
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
            i+= 1
        upperbound +=1
    return listCopy

temp = copy.copy(bubble(sys.argv))
for p in temp:
    print(p)