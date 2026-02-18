class A:
    def method_a(self):
        print("A method")

class B:
    def method_b(self):
        print("B method")

class C(A, B):
    pass

obj = C()
obj.method_a()
obj.method_b()