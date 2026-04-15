import re
a = input()
result = re.findall("[0-9][0-9]*[0-9]", a)
if len(result) == 0:
    print(" ")
else:
    for i in result:
        print(i, end=" ")