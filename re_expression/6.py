import re
text ="""my
name
is
Ramazan
"""
print(re.findall("^name", text, re.M))
print(re.findall("^name", text))