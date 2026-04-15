import re
a = input()
result = re.search("cat|dog", a)
if result:
    print(result.group())
else:
    print("No")
