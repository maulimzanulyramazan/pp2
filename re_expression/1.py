import re
b = int(input())
a = ""
for i in range(b):
    a = a + '.'
pattern = f"^a{a}s$"
test = input()
result = re.match(pattern, test)
if result:
    print("correct")
else:
    print("uncorrect")