import re
text = input()
text2 = input()
x = re.search("^my.*Ramazan$", text)
y = re.search(r"^i.*\d+", text2)
if x:
    print("true")
else:
    print("false")
if y:
    print(y.group())
else:
    print("not find")