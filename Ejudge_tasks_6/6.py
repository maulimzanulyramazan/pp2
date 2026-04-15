def NonNegative(n):
    if n >= 0:
        return True
    else:
        return False
a = int(input())
b = list(map(int, input().split()))
if all(NonNegative(x) for x in b):
    print("Yes")
else:
    print("No")