R = int(input())
a = []
for i in range(R):
    a.append(i)
for i in range(-R, 0):
    a.append(i)
x1, x2 = map(int, input().split())
x2, y2 = map(int, input().split())
summ = 0
if x1 > x2:
    for i in range(x2, x1):
        if i in a:
            summ = summ + 1
else:
    for i in range(x1, x2):
        if i in a:
            summ = summ + 1
print(f"{float(summ):.10f}")