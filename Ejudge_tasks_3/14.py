n = int(input())
a = input().split()
b = []
for i in range(n):
    b.append(int(a[i]))
q = int(input())
for i in range(q):
    command = input().split()
    if(command[0] == "abs"):
        for j in range(n):
            if(b[j] < 0):
                b[j] = b[j] * (-1)
    elif(command[0] == "add"):
        for j in range(n):
            b[j] = b[j] + int(command[1])
    elif(command[0] == "multiply"):
        for j in range(n):
            b[j] = b[j] * int(command[1])
    elif(command[0] == "power"):
        for j in range(n):
            b[j] = b[j] ** int(command[1])
print(*b)