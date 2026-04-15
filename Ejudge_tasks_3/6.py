class Rectangle():
    length = 0
    width = 0
    def calculatearea(self):
        print(self.length * self.width)
x = Rectangle()
nums = input().split()
x.length = int(nums[0])
x.width = int(nums[1])
x.calculatearea()
