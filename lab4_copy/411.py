import json
import sys
def apply(patch, source):
    for key, val in source.items():
        if val is None:
            patch.pop(key, None)
        elif key in patch and isinstance(patch[key], dict) and isinstance(val, dict):
            apply(patch[key], val)
        else:
            patch[key] = val
def main():
    lines = sys.stdin.read().splitlines()
    patch = json.loads(lines[0])
    source = json.loads(lines[1])
    apply(patch, source)
    print(json.dumps(patch, ensure_ascii = False, sort_keys = True, separators = (",",":")))
main()