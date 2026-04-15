class Reverse:
    def __init__(self, t):
        self.t = t
        self.index = len(t) - 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.index < 0:
            raise StopIteration
        ch = self.t[self.index]
        self.index -= 1
        return ch
t = input().strip()
rev = Reverse(t)
for ch in rev:
    print(ch, end="")