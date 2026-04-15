import sys
import time
import random

lyrics = [
    "Мойныңда сенің күмістен алқа",
    "Толқынды жаға",
    "Екеуміз ғана",
    "Сырымыз бітпей. Жалғасты таңға",
    "Жағымды жанға",
    "Менде арман бар ма? Ха."
]

def type_line(line: str, base_delay=0.045, jitter=0.03, comma_pause=0.15, dot_pause=0.25):
    """
    base_delay: әріптің орташа кідірісі
    jitter: кідірістің кездейсоқ ауытқуы (табиғи көріну үшін)
    comma_pause, dot_pause: тыныс белгілерінен кейін қосымша пауза
    """
    for ch in line:
        sys.stdout.write(ch)
        sys.stdout.flush()

        d = base_delay + random.uniform(-jitter, jitter)
        d = max(0.0, d)

        # тыныс белгілерін табиғи ету
        if ch in ",;:":
            d += comma_pause
        elif ch in ".!?":
            d += dot_pause
        elif ch == "\n":
            d += 0.05

        time.sleep(d)
    sys.stdout.write("\n")
    sys.stdout.flush()

def karaoke_typing(lines, line_pause=0.5):
    for line in lines:
        type_line(line)
        time.sleep(line_pause)

if __name__ == "__main__":
    karaoke_typing(lyrics, line_pause=0.6)