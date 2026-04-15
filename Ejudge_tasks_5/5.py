import re
a = input()
result = re.search("^[a-z].*[0-9]$", a, re.I)
if result:
    print("Yes")
else:
    print("No")