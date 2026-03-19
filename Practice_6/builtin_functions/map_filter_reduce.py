from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)

# reduce
total = reduce(lambda a, b: a + b, numbers)
print("Sum:", total)

# type checking and conversions
x = "123"
print("Type of x:", type(x))

y = int(x)
print("Converted y:", y)
print("Type of y:", type(y))

z = 45.67
print("Integer conversion:", int(z))
print("String conversion:", str(z))