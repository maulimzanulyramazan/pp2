n = int(input())
b = list(map(int, input().split()))
def NonZero(n):
    if n !=0:
        return True
    else:
        return False
result = map(NonZero, b)
print(sum(result))