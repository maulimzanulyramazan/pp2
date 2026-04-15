import json
a = input()
data = json.loads(a)
p = input()
b = int(input())
print(data["employees"][b][p])