import re
text = "Ääland"
text2 = "11 22 33"
print(re.findall(r"\w", text, re.A))
print(re.findall(r"\d+", text2, re.DEBUG))