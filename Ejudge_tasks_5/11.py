import re
a = input()
result = re.findall("[A-Z]", a)
print(len(list(result)))