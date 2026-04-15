import re
text = "Ramazan ramazan RAMAZAN"
text1= """my
name
is
Ramazan
"""
print(re.findall("ramazan", text, re.I))
print(re.findall("ramazan", text))
print(re.findall("my.name", text1, re.S))
print(re.findall("my.name", text1))