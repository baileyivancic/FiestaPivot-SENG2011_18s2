# EnsureCapacity and Duplicate were abstracted as Python's native
# list does not have any capacity.

class ArrayList:
    def __init__(self):
        self._array = []
        self._len = 0
        self._seqList = set()
        self._repr = set()

    def getSize(self):
        return self._len

    def isEmpty(self):
        return (self._len == 0)

    def get(self, counter):
        return self._array[int(counter)]

    def remove(self, counter):
        tmp = set(list(self._seqList)[0:counter])
        i = counter
        while i < self._len-1:
            self._array[i] = self._array[i+1]
            tmp.add(self._array[i])
            i = i + 1
        self._seqList = tmp
        self._array = self._array[0:-1]
        self._len = self._len - 1

    def append(self, element):
        self._array = self._array + [element]
        self._seqList = set(self._array)
        self._len = self._len + 1
        return self._len

if __name__ == '__main__':
    a = ArrayList()
    a.append(1)
    a.append(2)
    a.append(3)
    a.append('Hello')
    a.append(5)
    a.remove(2)
    print(a._array)