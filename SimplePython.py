import time as _time
import random as _random
import math as _math
import sys as _sys
import os as _os
import urllib.request as _urllib

# ============================================================
#  SIMPLEPYTHON v3.1 — Simplified Python Toolkit
#  Usage: import SimplePython
# ============================================================

# 1. SIMPLE BOOLEANS & EMPTY
yes = True
no = False
nothing = None

# 2. TALK, MENUS & INPUT SYSTEM (say.talk, say.ask, say.menu)
class _SaySystem:
    def talk(self, *args):
        print(*args)

    def type(self, text, speed=0.03):
        for char in str(text):
            print(char, end="", flush=True)
            _time.sleep(speed)
        print()

    def line(self):
        print("-" * 36)

    def space(self):
        print()

    def clear(self):
        _os.system("cls" if _os.name == "nt" else "clear")

    def ask(self, prompt):
        return input(str(prompt) + " ")

    def number(self, prompt):
        while True:
            try:
                return int(input(str(prompt) + " "))
            except ValueError:
                print("Please enter a valid number!")

    def yes_no(self, prompt):
        while True:
            ans = input(str(prompt) + " (yes/no): ").strip().lower()
            if ans in ("yes", "y"):
                return True
            if ans in ("no", "n"):
                return False
            print("Please type yes or no.")

    def menu(self, title, options):
        print(f"\n=== {title} ===")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        while True:
            choice = self.number("Choose option #:")
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Pick a number between 1 and {len(options)}.")

say = _SaySystem()

# 3. TIME & TIMER SYSTEM (time.wait, time.now, time.countdown)
class _TimeSystem:
    def wait(self, seconds):
        _time.sleep(seconds)

    def now(self):
        return _time.strftime("%I:%M %p")

    def today(self):
        return _time.strftime("%B %d, %Y")

    def countdown(self, seconds):
        for s in range(seconds, 0, -1):
            print(s)
            _time.sleep(1)

time = _TimeSystem()

# 4. MATH & LUCK SYSTEM (math.roll, math.luck, math.clamp)
class _MathSystem:
    def roll(self, low, high):
        return _random.randint(low, high)

    def luck(self, percent):
        return _random.randint(1, 100) <= percent

    def clamp(self, val, low, high):
        return max(low, min(high, val))

    def percent(self, part, total):
        return round((part / total) * 100, 1) if total != 0 else 0

    def root(self, val):
        return _math.sqrt(val)

math = _MathSystem()

# 5. LIST & TEXT HELPERS (lists.pick, text.clean)
class _ListSystem:
    def pick(self, items):
        return _random.choice(items)

    def shuffle(self, items):
        copy = list(items)
        _random.shuffle(copy)
        return copy

    def has(self, items, target):
        return target in items

lists = _ListSystem()

class _TextSystem:
    def clean(self, s):
        return str(s).strip()

    def lower(self, s):
        return str(s).lower()

    def upper(self, s):
        return str(s).upper()

    def has(self, s, word):
        return str(word) in str(s)

text = _TextSystem()

# 6. 1-LINE FILE SAVE & LOAD (files.save, files.load)
class _FileSystem:
    def save(self, filename, content):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(content))

    def load(self, filename, default=""):
        if not _os.path.exists(filename):
            return default
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    def load_number(self, filename, default=0):
        raw = self.load(filename, "").strip()
        return int(raw) if raw.isdigit() else default

    def exists(self, filename):
        return _os.path.exists(filename)

files = _FileSystem()

# 7. 1-LINE WEB FETCHER (web.get)
class _WebSystem:
    def get(self, url):
        with _urllib.urlopen(url) as response:
            return response.read().decode("utf-8")

web = _WebSystem()

# 8. INVENTORY / BAG HELPER (Bag)
class Bag:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        print(f"[+] Added '{item}' to bag.")

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"[-] Removed '{item}' from bag.")

    def has(self, item):
        return item in self.items

    def count(self):
        return len(self.items)

    def show(self):
        print(f"=== BAG ({len(self.items)} items) ===")
        if not self.items:
            print("  (Empty)")
        else:
            for item in self.items:
                print(f"  - {item}")

# 9. CUSTOM ERROR SYSTEM (error.warn, error.crash, error.check)
class _ErrorSystem:
    def warn(self, code, message):
        print(f"[SIMPLEPYTHON WARNING {code}]: {message}")

    def crash(self, code, message):
        print(f"\n[SIMPLEPYTHON ERROR {code}]: {message}")
        _sys.exit(1)

    def check(self, condition, code, message):
        if not condition:
            self.crash(code, message)

error = _ErrorSystem()

# ============================================================
#  AUTO-INJECT TOOLS ON `import SimplePython`
# ============================================================
_caller = _sys._getframe(1).f_globals
for _name in ("yes", "no", "nothing", "say", "time", "math", "lists", "text", "files", "web", "Bag", "error"):
    _caller.setdefault(_name, globals()[_name])
