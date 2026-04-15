n = int(input())
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])
maxcount = 0
count = 0
for i in range(n):
    for j in range(n):
        if(arr[i] == arr[j]):
            count = count + 1
    if(maxcount < count):
        maxcount = count
        c = arr[i]
    if(maxcount == count):
        if(c > arr[i]):
            c = arr[i]
    count = 0
print(c)