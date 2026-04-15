import datetime
a = input().split()
b = input().split()
parts = a[0].split('-')
parts1 = b[0].split('-')
sec1 = int(parts[0]) * 31536000 + int(parts[1]) * 2592000 + int(parts[2]) * 86400
sec2 = int(parts1[0]) * 31536000 + int(parts1[1]) * 2592000 + int(parts1[2]) * 86400
tz1 = a[1]
tz2 = b[1]
if '+' in tz1:
    tz11 = tz1.split('+')
    tz111 = tz11[1].split(':')
    sec1 = sec1 - (int(tz111[0]) * 3600)
else:
    tz11 = tz1.split('-')
    tz111 = tz11[1].split(':')
    sec1 = sec1 + (int(tz111[0]) * 3600)
if '+' in tz2:
    tz22 = tz2.split('+')
    tz222 = tz22[1].split(':')
    sec2 = sec2 - (int(tz222[0]) * 3600)
else:
    tz22 = tz2.split('-')
    tz222 = tz22[1].split(':')
    sec2 = sec2 + (int(tz222[0]) * 3600)
diff = abs(sec2 - sec1) // 86400
print(diff)