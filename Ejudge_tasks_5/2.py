import re
s = input()
p = input()
result = re.search(p, s)
if result:
    print("Yes")
else:
    print("No")