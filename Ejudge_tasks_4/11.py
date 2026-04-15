import json
import sys

def apply_patch(source, patch):
    for keyy, vall in patch.items():
        if vall is None:
            source.pop(keyy, None)
        elif keyy in source and isinstance(source[keyy], dict) and isinstance(vall, dict):
            apply_patch(source[keyy], vall)
        else:
            source[keyy] = vall
def main():
    lines = sys.stdin.read().splitlines()
    source = json.loads(lines[0])
    patch = json.loads(lines[1])
    apply_patch(source, patch)
    print(json.dumps(source, ensure_ascii=False , sort_keys = True, separators=(',', ':')))
main()