import json
import sys

MISSING = object()

def to_json_literal(v):
    if v is MISSING:
        return "<missing>"
    # compact JSON literal
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'))

def differences(a, b, path="", out=None):
    if out is None:
        out = []

    # Егер екеуі де dict болса — ішіне кіреміз
    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())  # union
        for key in keys:
            new_path = f"{path}.{key}" if path else key
            aval = a.get(key, MISSING)
            bval = b.get(key, MISSING)
            differences(aval, bval, new_path, out)
        return out

    # dict емес болса — тікелей салыстырамыз
    if a != b:
        out.append(f"{path} : {to_json_literal(a)} -> {to_json_literal(b)}")

    return out

def main():
    text = sys.stdin.buffer.read().decode("utf-8-sig")  # BOM-ды автомат кетіреді
    lines = text.splitlines()

    A = json.loads(lines[0])
    B = json.loads(lines[1])

    out = differences(A, B)
    out.sort()  # path бойынша лексикографиялық сорт

    if not out:
        print("No differences")
    else:
        print("\n".join(out))

if __name__ == "__main__":
    main()