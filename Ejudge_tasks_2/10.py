n = int(input())
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])
mn = arr[0]
mx = arr[0]
for i in range(n):
    for y in range(n):
        if(arr[y] < arr[i]):
            temp = arr[i]
            arr[i] = arr[y]
            arr[y] = temp
for x in arr:
    print(x, end=" ")