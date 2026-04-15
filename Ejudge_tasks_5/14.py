import re
a = input()
pattern = re.compile(r"^\d+$")
result = pattern.match(a)
if result:
    print("Match")
else:
    print("No match")