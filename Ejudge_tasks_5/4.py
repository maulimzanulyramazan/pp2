import re
a = input()
pattern = r"\d"
result = re.findall(pattern, a)
if len(list(result)) == 0:
    print("no digits here")
else:
    for i in result:
        print(i, end=" ")