def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
s, t = input().split()
s = int(s)
t = int(t)
for x in squares(s, t):
    print(x)