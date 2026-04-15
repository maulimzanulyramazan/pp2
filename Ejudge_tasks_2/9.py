n = int(input())
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])
mx = arr[0]
mn = arr[0]
for x in arr:
    if x > mx:
        mx = x
    if x < mn:
        mn = x
for i in range(n):
    if arr[i] == mx:
        arr[i] = mn

for x in arr:
    print(x, end=" ")
