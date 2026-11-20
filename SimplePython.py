import os
import sys
import re
import time
import random

# ============================================================
#  1. SIMPLIFIED BUILT-IN HELPERS
# ============================================================
yes = True
no = False

def say(*args):
    print(*args)

def ask(prompt):
    return input(str(prompt) + " ")

def ask_number(prompt):
    while True:
        try:
            return int(input(str(prompt) + " "))
        except ValueError:
            print("Please enter a valid whole number!")

def wait(seconds):
    time.sleep(seconds)

def roll(low, high):
    return random.randint(low, high)

def luck(percent):
    return random.randint(1, 100) <= percent

def clamp(val, low, high):
    return max(low, min(high, val))


# ============================================================
#  2. BRACE-TO-INDENTATION TRANSLATOR (Zero Indentation!)
# ============================================================
def translate_simple_python(source: str) -> str:
    output = ["from SimplePython import *\n"]
    indent = 0

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        while line.startswith("}"):
            indent = max(0, indent - 1)
            line = line[1:].strip()

        if not line:
            continue

        line = re.sub(r'\botherwise\b', 'else', line)
        line = re.sub(r'\belse if\b', 'elif', line)
        line = re.sub(r'\baction\s+', 'def ', line)
        line = re.sub(r'\brepeat\s*\((.+?)\)\s*\{', r'for _rep in range(\1): {', line)

        if line.endswith("{"):
            header = line[:-1].strip()
            if not header.endswith(":"):
                header += ":"
            output.append(("    " * indent) + header)
            indent += 1
        else:
            output.append(("    " * indent) + line)

    return "\n".join(output)


# ============================================================
#  3. SMART .SP FILE FINDER & RUNNER
# ============================================================
def find_sp_file(target_name=None):
    # If a specific .sp filename was given, check direct path first, then search subfolders!
    if target_name:
        if not target_name.endswith(".sp"):
            raise ValueError(f"[SimplePython Error]: '{target_name}' must end with '.sp'!")
        if os.path.isfile(target_name):
            return target_name
        for root, _, files in os.walk("."):
            if target_name in files:
                return os.path.join(root, target_name)
        raise FileNotFoundError(f"[SimplePython Error]: Could not find '{target_name}' anywhere in this project!")

    # If no filename was given, hunt down all .sp files in the project!
    found = []
    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".sp"):
                found.append(os.path.join(root, f))

    if not found:
        raise FileNotFoundError("[SimplePython Error]: No .sp file found! Create any file ending in '.sp' (e.g. bot.sp).")
    if len(found) == 1:
        return found[0]
    for path in found:
        if os.path.basename(path) == "main.sp":
            return path
    return found[0]

def run_code(code: str):
    translated = translate_simple_python(code)
    exec(compile(translated, "<SimplePython>", "exec"), {})

def run_file(filename=None):
    filepath = find_sp_file(filename)
    with open(filepath, "r", encoding="utf-8") as f:
        run_code(f.read())

# Alias so people can simply type SimplePython.run("bot.sp") or SimplePython.run()!
run = run_file

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) >= 2 else None
    run_file(target)
