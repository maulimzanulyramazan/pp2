import sys

def main():
    data = sys.stdin.read().strip().split()
    x1, y1, x2, y2 = map(float, data)

    # If both points are on the mirror (degenerate), any x works; choose x1.
    if abs(y1) < 1e-12 and abs(y2) < 1e-12:
        print(f"{x1:.10f} {0.0:.10f}")
        return

    t = y1 / (y1 + y2)
    x = x1 + t * (x2 - x1)

    print(f"{x:.10f} {0.0:.10f}")

if __name__ == "__main__":
    main()