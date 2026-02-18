class Math:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def hello(cls):
        print("Hello from classmethod:", cls.__name__)

print(Math.add(3, 4))
Math.hello()