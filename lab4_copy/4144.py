from datetime import datetime, timedelta
a = input().split()
b = input().split()
dt1 = datetime.strptime(a[0], '%Y-%m-%d')
dt2 = datetime.strptime(b[0], '%Y-%m-%d')
tz1 = a[1]
tz2 = b[1]
if '+' in tz1:
    h, m = map(int, tz1.split('+')[1].split(':'))
    dt1 = dt1 - timedelta(hours = h, minutes = m)
else:
    h, m = map(int, tz1.split('-')[1].split(':'))
    dt1 = dt1 + timedelta(hours = h , minutes = m)
if '+' in tz2:
    h, m = map(int, tz2.split('+')[1].split(':'))
    dt2 = dt2 - timedelta(hours = h, minutes = m)
else:
    h, m = map(int, tz2.split('-')[1].split(':'))
    dt2 = dt2 + timedelta(hours = h , minutes = m)
print(int(abs((dt2 - dt1).total_seconds()) // 86400))