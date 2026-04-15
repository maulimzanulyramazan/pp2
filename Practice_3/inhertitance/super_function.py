class Person:
    def __init__(self, name):
        self.name = name

class Worker(Person):
    def __init__(self, name, job):
        super().__init__(name)
        self.job = job

w = Worker("Ramazan", "Developer")
print(w.name, w.job)