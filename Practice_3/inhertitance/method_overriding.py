class Bird:
    def fly(self):
        print("Bird flies")

class Penguin(Bird):
    def fly(self):
        print("Penguin can't fly")

b = Bird()
p = Penguin()

b.fly()
p.fly()