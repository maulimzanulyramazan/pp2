def val(number):
    while(number >= 1):
        if (number % 10) % 2 == 0:
            number = number // 10
        else:
            return "Not valid"
    return "Valid"
print(val(int(input())))