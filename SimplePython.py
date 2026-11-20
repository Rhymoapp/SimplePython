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
#  2. BRACE-TO-INDENTATION TRANSLATOR (Kills Indentation!)
# ============================================================
def translate_simple_python(source: str) -> str:
    output = ["from SimplePython import *\n"]
    indent = 0

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        # Handle closing braces '}'
        while line.startswith("}"):
            indent = max(0, indent - 1)
            line = line[1:].strip()

        if not line:
            continue

        # Translate simplified keywords into valid Python
        line = re.sub(r'\botherwise\b', 'else', line)
        line = re.sub(r'\belse if\b', 'elif', line)
        line = re.sub(r'\baction\s+', 'def ', line)
        line = re.sub(r'\brepeat\s*\((.+?)\)\s*\{', r'for _rep in range(\1): {', line)

        # Handle opening braces '{'
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
#  3. RUNNERS (Single-File Mode or .sp File Mode)
# ============================================================
def run(code: str):
    translated = translate_simple_python(code)
    exec(compile(translated, "<SimplePython>", "exec"), {})

def run_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        run(f.read())
