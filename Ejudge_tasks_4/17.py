import math
import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    R = float(data[0])
    x1, y1 = float(data[1]), float(data[2])
    x2, y2 = float(data[3]), float(data[4])

    dx = x2 - x1
    dy = y2 - y1

    a = dx*dx + dy*dy
    # If A == B, segment length is 0 anyway
    if a == 0.0:
        print("0.0")
        return

    b = 2.0 * (x1*dx + y1*dy)
    c = x1*x1 + y1*y1 - R*R

    disc = b*b - 4.0*a*c
    seg_len = math.sqrt(a)

    # No intersection with circle boundary
    if disc < 0.0:
        # If A is inside, whole segment is inside; else none
        if c <= 0.0:
            print(f"{seg_len:.10f}")
        else:
            print(f"{0.0:.10f}")
        return

    sqrt_disc = math.sqrt(max(0.0, disc))
    t1 = (-b - sqrt_disc) / (2.0 * a)
    t2 = (-b + sqrt_disc) / (2.0 * a)
    if t1 > t2:
        t1, t2 = t2, t1

    left = max(0.0, t1)
    right = min(1.0, t2)

    inside_t = max(0.0, right - left)
    ans = inside_t * seg_len
    print(f"{ans:.10f}")

if __name__ == "__main__":
    main()