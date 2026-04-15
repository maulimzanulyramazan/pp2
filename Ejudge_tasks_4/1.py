def squares(n):
    for i in range(1, n + 1):
        yield i * i
t = int(input())
for x in squares(t):
    print(x)