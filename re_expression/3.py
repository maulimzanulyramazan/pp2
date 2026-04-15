import re
text = "i come from Aktobe and I live here 6 months"
print(re.findall("[a-m]", text))
print(re.findall("Akt..e", text))
print(re.findall("^i", text))
print(re.findall("months$", text))
print((re.search("Aktob.*e", text)).group())
print((re.search("Akto.+e", text)).group())
print(re.findall("Akt.?be", text))
print(re.findall("mo.{3}s", text))
print(re.findall("and|or", text))
print(re.findall(r"\d+", text))