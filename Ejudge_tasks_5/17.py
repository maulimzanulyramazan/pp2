import re
a = input()
result = re.findall(r"[0-9]+/[0-9]+/[0-9]+", a)
print(len(result))