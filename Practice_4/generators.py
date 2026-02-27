def even_numbers():
    x = 0
    while True:  #created squares of all natural numbers from zero to infinity
        yield x ** 2
        x = x + 1
# Create a generator object
gen = even_numbers()

# Get values one by one using next()
for i in range(int(input()) + 1):
    print(next(gen), end=" ")  

def Evens(n): 
    for i in range(n + 1):
        if(i % 2 == 0):
            yield i  #return to as value if it is even
gen1 = Evens(int(input())) #all even numbers from 0 to n
for y in gen1:
    print(y, end=" ")    