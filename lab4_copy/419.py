x = int(input())
for i in range(x):
    try:
        print(10 / i)
    except:
        print("10 is not divisible to 0")