def fibbonaci(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b
p = int(input())
for y in fibbonaci(p):
    if(y == 0):
        print(y, end="")
    else:
        print(f",{y}", end= "")