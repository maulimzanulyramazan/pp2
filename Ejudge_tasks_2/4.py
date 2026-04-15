n = int(input())
a = list(map(int, input().split()))
x = 0
for i in a:
    if i > 0:
        x = x + 1
print(x)