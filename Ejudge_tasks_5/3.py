import re
a = input()
b = input()
matches = re.findall(b, a)
print(len(matches))