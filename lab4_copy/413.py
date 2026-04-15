import json

data = json.loads(input())
q = int(input())

for i in range(q):
    query = input()
    
    cur = data
    ok = True
    parts = query.split('.')
    
    for p in parts:
        try:
            # егер [index] бар болса
            while '[' in p:
                key = p[:p.index('[')]
                if key:
                    cur = cur[key]
                
                idx = int(p[p.index('[')+1:p.index(']')])
                cur = cur[idx]
                
                p = p[p.index(']')+1:]
            
            if p:
                cur = cur[p]
        
        except:
            ok = False
            break
    
    if ok:
        print(json.dumps(cur))
    else:
        print("NOT_FOUND")