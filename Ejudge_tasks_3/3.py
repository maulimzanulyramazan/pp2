m = {
    "ZER": "0",
    "ONE": "1",
    "TWO": "2",
    "THR": "3",
    "FOU": "4",
    "FIV": "5",
    "SIX": "6",
    "SEV": "7",
    "EIG": "8",
    "NIN": "9"
}
r = {}
for k in m:
    r[m[k]] = k
s = input()
if '+' in s:
    op = '+'
elif '-' in s:
    op = '-'
else:
    op = '*'
parts = s.split(op)
a = parts[0]
b = parts[1]
num1 = ""
i = 0
while i < len(a):
    num1 += m[a[i:i+3]]
    i += 3
num2 = ""
i = 0
while i < len(b):
    num2 += m[b[i:i+3]]
    i += 3
num1 = int(num1)
num2 = int(num2)
if op == '+':
    res = num1 + num2
elif op == '-':
    res = num1 - num2
else:
    res = num1 * num2
ans = ""
for d in str(res):
    ans += r[d]

print(ans)