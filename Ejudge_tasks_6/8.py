a = int(input())
b = list(map(int, input().split()))
b_set = set(b)
for i in sorted(b_set):
    print(i, end=" ")