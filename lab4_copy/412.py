import json
import sys
path = ""
def Deepdiff(patch, source):
    global path
    for key, val in source.items():
        if key in patch and isinstance(patch[key], dict) and isinstance(val, dict):
            if(path == ""):
                path = path + key
            else:
                path = path + "." + key
            Deepdiff(patch[key], val)
        elif patch[key] != val:
            if(path == ""):
                path = path + key
            else:
                path = path + "." + key
            print(f"{path} : {patch[key]} -> {val}")
    if patch == source:
        print("No differences")
def main():
    lines = sys.stdin.read().splitlines()
    patch = json.loads(lines[0])
    source = json.loads(lines[1])
    Deepdiff(patch, source)
main()