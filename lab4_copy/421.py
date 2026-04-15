q = int(input())
for i in range(q):
    module_path, attr = input().split()
    
    try:
        module = __import__(module_path, fromlist = ('*'))
    except:
        print("MODULE_NOT_FOUND")
        continue
    if hasattr(module, attr):
        value = getattr(module, attr)
        if callable(value):
            print("CALLABLE")
        else:
            print("VALUE")
    else:
        print("ATTRIBUTE_NOT_FOUND")
