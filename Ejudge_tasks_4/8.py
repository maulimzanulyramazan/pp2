n = int(input())
a = [2]
x = 2
b = 0
for i in range(3, n + 1):
    while(x < i):
        if(i % x == 0):
            b = b + 1
        x = x + 1
    if b > 0:
        x = 2
        b = 0
        continue
    else:
        a.append(i)
    x = 2
    b = 0
if n == 1 or n == 0:
    print()
else:
    print(*a)