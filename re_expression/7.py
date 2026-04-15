import re
text = "now 17:00 but after 1 hour will be 18:00"
result = re.split(r"\d", text)
print(result)
text1 = 'abc 12\
    de 23 \n f45 6'
pattern1 = r"\s+"
replace1 = ''
print(re.sub(pattern1, replace1, text1, 5))
print(re.subn(pattern1, replace1, text1))