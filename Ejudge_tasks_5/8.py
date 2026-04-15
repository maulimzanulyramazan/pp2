import re
s = input()
pattern = input()
result = re.sub(pattern, ',', s)
print(result)