import re
a = input()
res = re.findall(r"\d", a)
result = list(res)
for i in range(len(result)):
    res[i] = res[i] * 2
for i in res:
    print(i, end='')