n = int(input())
a = 2
x = 0
while(a < n):
    if(n % a == 0):
        print("No")
        x = x + 1
        break
    a = a + 1
if(x == 0):
    print("Yes")