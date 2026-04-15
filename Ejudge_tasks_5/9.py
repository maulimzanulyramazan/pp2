import re
a = input()
count = 0
result = re.split(r"\s", a)
for i in result:
    if len(i) == 3:
        count += 1
print(count)