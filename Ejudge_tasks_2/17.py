n = int(input())
arr = []
for i in range(n):
    a = input()
    arr.append(a)
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1
count = sum(1 for y in freq.values() if y == 3)
print(count)