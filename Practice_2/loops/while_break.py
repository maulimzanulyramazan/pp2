n = int(input())
while(n > 1):
    if(n % 2 != 0):
        print(f"half of n is {n / 2} is not even number")
        break
    print(f"half of n is {n // 2} is even number, let's devide it to 2 again")
    n = n // 2