import sys
n = int(sys.stdin.readline())
thisdict = {}
for i in range(n):
    com = sys.stdin.readline().split()
    if com[0] == "set":
        ke, val = com[1], com[2]
        thisdict[ke] = val
    if com[0] == "get":
        ke = com[1]
        if ke in thisdict:
            print(thisdict[ke])
        else:
            print(f"KE: no key {ke} found in the document")