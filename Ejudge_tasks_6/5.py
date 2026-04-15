a = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
s = input()
if any(i in a for i in s):
    print("Yes")
else:
    print("No")