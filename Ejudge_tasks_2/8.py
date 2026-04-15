n = int(input())
x = 1
y = 1
a = []
while(y <= n):
    a.append(y)
    y = 2 ** x
    x = x + 1
print(*a)