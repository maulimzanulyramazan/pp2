n = int(input())
nums = list(map(int, input().split()))
def Evens(n):
    if n % 2 == 0:
        return True
    else:
        return False
result = list(filter(Evens, nums))
print(len(result))