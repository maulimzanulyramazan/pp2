year = int(input())
if(year % 400 == 0):
    print("YES")
elif(year % 100 == 0):
    print("NO")
elif(year % 4 == 0):
    print("YES")
else:
    print("NO")