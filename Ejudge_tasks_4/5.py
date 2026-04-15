def nums(n):
    t = n
    for i in range(t + 1):
        yield n
        n = n - 1
x = int(input())
for y in nums(x):
    print(y)