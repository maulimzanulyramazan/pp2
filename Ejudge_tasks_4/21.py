import sys
import importlib

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return

    q = int(data[0].strip())
    out = []

    for i in range(1, q + 1):
        line = data[i].strip()
        if not line:
            out.append("MODULE_NOT_FOUND")  # defensive, shouldn't happen
            continue

        module_path, attr = line.split()

        try:
            mod = importlib.import_module(module_path)
        except (ModuleNotFoundError, ImportError):
            out.append("MODULE_NOT_FOUND")
            continue

        if not hasattr(mod, attr):
            out.append("ATTRIBUTE_NOT_FOUND")
            continue

        value = getattr(mod, attr)
        out.append("CALLABLE" if callable(value) else "VALUE")

    print("\n".join(out))

if __name__ == "__main__":
    main()