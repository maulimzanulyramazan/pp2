class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def info(self):
        print(f"{self.name}: grade {self.grade}")

s1 = Student("Ramazan", 100)
s1.info()