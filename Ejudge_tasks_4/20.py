m = int(input().strip())

g = 0
n = 0

for _ in range(m):
    scope, value = input().split()
    x = int(value)

    if scope == "global":
        g += x
    elif scope == "nonlocal":
        n += x
    # scope == "local" -> ignore

print(g, n)