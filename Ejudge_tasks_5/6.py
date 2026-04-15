import re
a = input()
b = 0
result = re.split(r"\s", a)
for i in list(result):
    if "@" in i:
        print(i)
        b = b + 1
        break
if b == 0:
    print("No email")