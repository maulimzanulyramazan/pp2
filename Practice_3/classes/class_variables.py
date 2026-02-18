class Car:
    wheels = 4

    def __init__(self, brand):
        self.brand = brand

c1 = Car("Toyota")
c2 = Car("BMW")

print(c1.brand, c1.wheels)
print(c2.brand, c2.wheels)

Car.wheels = 6
print("After change:", c1.wheels, c2.wheels)