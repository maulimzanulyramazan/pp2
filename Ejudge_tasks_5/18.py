import re
a = input()
b = input()
result = re.findall(re.escape(b),  a)
print(len(result))