def fibbonaci(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b
t = int(input())
for i in fibbonaci(t):
    if(i == 0):
        print(i, end="")
    else:
        print(f", {i}", end="")