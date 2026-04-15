def pairs(a, x, b, y):
    sum1 = int(a) + int(b)
    sum2 = int(x) + int(y)
    print(f"Result: {sum1} {sum2}")
w = input().split()
pairs(w[0], w[1], w[2], w[3])