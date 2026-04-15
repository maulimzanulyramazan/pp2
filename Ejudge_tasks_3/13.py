def NonPrime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
a = list(map(int, input().split()))
noprime = list(filter(lambda x : NonPrime(x) , a))
if len(noprime) == 0:
    print("No primes")
else:
    print(*noprime)