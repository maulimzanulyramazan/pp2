inputs = input().split()
n = int(inputs[0])
l = int(inputs[1]) 
r = int(inputs[2]) 
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])
while(l < r):
    temp = arr[l - 1]
    arr[l - 1] = arr[r - 1]
    arr[r - 1] = temp
    l = l + 1
    r = r - 1
for x in arr:
    print(x, end=" ")
    