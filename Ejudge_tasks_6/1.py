def Squares(n):
    return n * n
a = int(input())
nums = list(map(int, input().split()))
result = map(Squares, nums)
sum = 0
for i in list(result):
    sum += i
print(sum)