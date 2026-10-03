"""Generate Municipality Tycoon license keys.
Usage: python tools/make_license.py [count]
Keys are checked client-side, so they only deter casual copying. For real protection, sell the full
game as a separate download or validate keys on a server. Keep LICENSE_SALT in sync with index.html."""
import random, string, sys

SALT = "mt-clifton-2026"

def fnv(s):
    h = 2166136261
    for c in s:
        h ^= ord(c)
        h = (h * 16777619) & 0xFFFFFFFF
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while h:
        out = digits[h % 36] + out
        h //= 36
    return (out or "0").upper()

def make():
    alphabet = string.ascii_uppercase + string.digits
    a = "".join(random.choice(alphabet) for _ in range(4))
    b = "".join(random.choice(alphabet) for _ in range(4))
    return f"MT-{a}-{b}-{fnv(a + '-' + b + SALT)}"

if __name__ == "__main__":
    for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 5):
        print(make())
