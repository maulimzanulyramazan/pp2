n = int(input())
arr = input().split()
a = []
for i in range(n):
    arr[i] = int(arr[i])
for i in range(n):
    if arr[i] in a:
        print("NO")
        continue
    else:
        print("YES")
        a.append(arr[i])