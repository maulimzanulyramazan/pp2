text = input()
a = ""
x = len(text)
while(x > 0):
    a = a + text[x - 1]
    x = x - 1
print(a)