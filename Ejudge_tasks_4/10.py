def Cycle(x):
    while True:
        yield x
gen = Cycle(input())
for i in range(int(input())):
    print(next(gen), end=" ")