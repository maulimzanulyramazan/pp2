def Squares():
    x = 0
    a = 2
    while True:
        yield a ** x
        x = x + 1
gen = Squares()
for i in range(int(input()) + 1):
    print(next(gen), end=" ")