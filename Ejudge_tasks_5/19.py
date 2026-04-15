import re
a = input()
result = re.findall(r"\b\w+\b", a)
print(len(result))
