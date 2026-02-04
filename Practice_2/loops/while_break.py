n = int(input())
while(n > 1):
    if(n % 2 != 0):
        print(f"{n / 2} is half of n so n is not even number")
        break
    print(f"{n // 2} is half of n, so n is even number, let's devide it to 2 again")
    n = n // 2