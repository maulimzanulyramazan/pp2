import re
a = input()
b = re.match("^Hello", a)
if b:
    print("Yes")
else:
    print("No")