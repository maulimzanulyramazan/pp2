import re
a = input()
result = re.findall(r"\w+", a)
print(len(result))