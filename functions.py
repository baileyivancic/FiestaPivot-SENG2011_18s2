# Temp file for all functions converted to python
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

# Bubble sort to sort ads by date 
def bubbleDateAds(args):
    listCopy = copy.copy(args)
    i = (len(args) -1)
    upperbound = 0
    while (upperbound < len(args)):
        i = (len(args) - 1)
        while (i > upperbound):
            if (listCopy[i-1][8] > listCopy[i][8]):
                temp = listCopy[i]
                listCopy[i] = listCopy[i - 1]
                listCopy[i - 1] = temp
            i-= 1
        upperbound +=1
    return listCopy

# Bubble sort to sort ads by price
def bubblePriceAds(args):
    listCopy = copy.copy(args)
    i = (len(args) -1)
    upperbound = 0
    while (upperbound < len(args)):
        i = (len(args) - 1)
        while (i > upperbound):
            if (listCopy[i-1][3] > listCopy[i][3]):
                temp = listCopy[i]
                listCopy[i] = listCopy[i - 1]
                listCopy[i - 1] = temp
            i-= 1
        upperbound +=1
    return listCopy

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

# def quicksort(a=[], left, right):
#     if left < (right-1):
#         p = partition(a, left, right)
#         quicksort(a, left, p)
#         quicksort(a, p+1, right)

# def partition(b=[], left, right):
#     p = left
#     k = left+1

#     while k < right:
#         if a[k] < a[p]:
#             j = k+1
#             tmp = a[k]
#             a[k] = a[j]
            
#             while j < p:
#                 a[j+1] = a[j]
#                 j+=1

#             a[p+1] = a[p]
#             p+=1 
#             a[p-1] = tmp

#         k+=1