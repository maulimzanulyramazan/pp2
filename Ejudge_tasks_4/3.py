def devisible(n):
    t = 0
    while t <= n:
        yield t
        t = t + 12
s = int(input())
for x in devisible(s):
    print(x, end =" ")