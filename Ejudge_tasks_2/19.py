n = int(input())
thisdict = {}
for i in range(n):
    ke, val = input().split()
    val = int(val)
    if ke in thisdict:
        thisdict[ke] = thisdict[ke] + val
    else:
        thisdict[ke] = val
for serial in sorted(thisdict.keys()):
    print(serial, thisdict[serial])