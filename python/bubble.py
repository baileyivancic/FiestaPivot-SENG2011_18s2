# Written by Bailey Ivancic - converted from Dafny verified code written by Harry Tang and Nabil Shaikh
import sys

def test():
    temp = list(bubble(sys.argv))
    for p in temp:
        print(p)

def bubble(list):
    listCopy = list.copy()
    i = (len(list) -1)
    upperbound = 0
    while (upperbound < len(list)):
        i = (len(list) - 1)
        while (i > upperbound):
            if (listCopy[i-1] > listCopy[i]):
                temp = listCopy[i]
                listCopy[i] = listCopy[i - 1]
                listCopy[i - 1] = temp
            i+= 1
        upperbound +=1
    return listCopy