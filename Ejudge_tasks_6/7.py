a = int(input())
b = list(map(str, input().split()))
print(max(b, key=len))