n = int(input())
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])
for i in range(n):
    arr[i] = arr[i] ** 2
for x in arr:
    print(x, end=" ")