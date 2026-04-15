import json
import sys

def to_compact_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))

def parse_query(q: str):
    """
    Query-ді токендерге бөледі:
    "user.friends[2].name" -> ["user", "friends", 2, "name"]
    "x[1]" -> ["x", 1]
    "a.b.c" -> ["a", "b", "c"]
    """
    tokens = []
    i = 0
    n = len(q)

    while i < n:
        ch = q[i]

        if ch == '.':
            i += 1
            continue

        if ch == '[':
            # индекс оқу
            j = i + 1
            if j >= n:
                return None  # жарамсыз
            # тек цифрлар күтеміз
            if q[j] == ']':
                return None
            while j < n and q[j] != ']':
                if not q[j].isdigit():
                    return None
                j += 1
            if j >= n or q[j] != ']':
                return None
            idx = int(q[i+1:j])
            tokens.append(idx)
            i = j + 1
            continue

        # key оқу ('.' немесе '[' дейін)
        j = i
        while j < n and q[j] not in '.[':
            j += 1
        key = q[i:j]
        if key == "":
            return None
        tokens.append(key)
        i = j

    return tokens

def resolve_query(data, query: str):
    tokens = parse_query(query)
    if tokens is None:
        return None, False

    cur = data
    for t in tokens:
        if isinstance(t, str):
            # dict key
            if not isinstance(cur, dict):
                return None, False
            if t not in cur:
                return None, False
            cur = cur[t]
        else:
            # list index
            if not isinstance(cur, list):
                return None, False
            if t < 0 or t >= len(cur):
                return None, False
            cur = cur[t]

    return cur, True

def main():
    text = sys.stdin.buffer.read().decode("utf-8-sig")
    lines = text.splitlines()

    J = json.loads(lines[0])
    q = int(lines[1])

    out_lines = []
    for i in range(q):
        query = lines[2 + i].strip()
        value, ok = resolve_query(J, query)
        if ok:
            out_lines.append(to_compact_json(value))
        else:
            out_lines.append("NOT_FOUND")

    print("\n".join(out_lines))

if __name__ == "__main__":
    main()