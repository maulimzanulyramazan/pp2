def isUsual(num):
    while(num % 5 == 0 or num % 2 == 0 or num % 3 == 0):
        if(num % 5 == 0):
            num = num // 5
        if(num % 2 == 0):
            num = num // 2
        if(num % 3 == 0):
            num = num // 3
    if num > 1:
        print("No")
    else:
        print("Yes")
isUsual(int(input()))