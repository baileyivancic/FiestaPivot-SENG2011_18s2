def quicksort(a, left, right):
   if left < right - 1:
      p = partition(a, left, right)
      quicksort(a, left, p)
      quicksort(a, p+1, right)

def partition(a, left, right):
    p = left
    k = left + 1

    while k < right:
        if a[k] < a[p]:
            j = k - 1
            tmp = a[k]
            a[k] = a[j]

            while j < p:
                a[j+1] = a[j]
                j = j - 1
        
            a[p+1] = a[p]
            p = p + 1
            a[p-1] = tmp
        k = k + 1
    return p

if __name__ == '__main__':
    a = [5,4,3,2,1]
    quicksort(a,0,len(a))
    print(a)