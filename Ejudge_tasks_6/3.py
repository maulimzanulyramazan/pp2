a = int(input())
b = list(map(str, input().split()))
result = enumerate(b)
for index, word in result:
    print(f"{index}:{word}", end=" ")