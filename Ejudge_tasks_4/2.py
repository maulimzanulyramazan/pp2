def evens(n):
    t = 0
    while 0 <= t <= n:
        yield t
        t = t + 2
x = int(input())
for x in evens(x):
    if(x == 0):
        print(x, end="")
    else:
        print(f",{x}", end="")