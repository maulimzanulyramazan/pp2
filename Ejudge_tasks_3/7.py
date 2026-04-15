class cordinates():
    x = 0
    y = 0
    new_x = 0
    new_y = 0
    x3 = 0
    y3 = 0
    def calculated(self):
        print(f"({self.x}, {self.y})")
        print(f"({self.new_x}, {self.new_y})")
        distance = ((self.x3 - self.new_x) ** 2 + (self.y3 - self.new_y) ** 2) ** 0.5
        print(f"{distance:.2f}")
cord = cordinates()
first = input().split()
cord.x = (first[0])
cord.y = int(first[1])
second = input().split()
cord.new_x = int(second[0])
cord.new_y = int(second[1])
third = input().split()
cord.x3 = int(third[0])
cord.y3 = int(third[1])
cord.calculated()