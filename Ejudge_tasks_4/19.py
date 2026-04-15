import math
import sys

def dist(x, y):
    return math.hypot(x, y)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def segment_intersects_circle(ax, ay, bx, by, R):
    # AB кесіндісінің O(0,0) центрден ең жақын нүктесіне дейінгі қашықтықты табамыз
    vx, vy = bx - ax, by - ay
    wx, wy = -ax, -ay  # O - A

    vv = vx*vx + vy*vy
    if vv == 0.0:
        # A==B
        return dist(ax, ay) < R

    t = (wx*vx + wy*vy) / vv  # проекция параметрі
    t = clamp(t, 0.0, 1.0)

    px = ax + t*vx
    py = ay + t*vy

    return dist(px, py) < R  # strict < R болса "ішіне кірді" деп аламыз

def main():
    data = sys.stdin.read().strip().split()
    R = float(data[0])
    x1, y1 = float(data[1]), float(data[2])
    x2, y2 = float(data[3]), float(data[4])

    # Егер түзу жол шеңбердің ішіне кірмесе -> AB
    if not segment_intersects_circle(x1, y1, x2, y2, R):
        ans = math.hypot(x2 - x1, y2 - y1)
        print(f"{ans:.10f}")
        return

    d1 = dist(x1, y1)
    d2 = dist(x2, y2)

    # жанама кесінділері
    t1 = math.sqrt(max(0.0, d1*d1 - R*R))
    t2 = math.sqrt(max(0.0, d2*d2 - R*R))

    # phi = angle between OA and OB
    dot = x1*x2 + y1*y2
    cos_phi = clamp(dot / (d1 * d2), -1.0, 1.0)
    phi = math.acos(cos_phi)

    alpha = math.acos(clamp(R / d1, -1.0, 1.0))
    beta  = math.acos(clamp(R / d2, -1.0, 1.0))

    theta = max(0.0, phi - alpha - beta)

    ans = t1 + t2 + R * theta
    print(f"{ans:.10f}")

if __name__ == "__main__":
    main()