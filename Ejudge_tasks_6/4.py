n = int(input())
line1 = list(map(int, input().split()))
line2 = list(map(int, input().split()))
result = zip(line1, line2)
sum = 0
for i, j in list(result):
    sum = sum + (i*j)
print(sum)