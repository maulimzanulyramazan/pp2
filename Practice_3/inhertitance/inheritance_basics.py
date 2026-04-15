class Animal:
    def speak(self):
        print("Some sound")

class Cat(Animal):
    pass

c = Cat()
c.speak()