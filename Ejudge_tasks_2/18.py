n = int(input())
arr = []
arr11 = []
pairs = []
for i in range(n):
    a = input()
    arr.append(a)
for i in range(n):
    if arr[i] in arr11:
        continue
    else:
        arr11.append(arr[i])
        pairs.append((arr[i], i + 1))
pairs.sort()
for x, y in pairs:
    print(x, y)