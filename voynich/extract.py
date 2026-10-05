"""Extract one transcriber's text from the interlinear EVA file.

Usage: python extract.py [TRANSCRIBER]   (default: H = Takahashi, the complete one)
Writes takahashi.txt-style output: one line per manuscript line, "<locus> text".
"""
import re
import sys

who = sys.argv[1] if len(sys.argv) > 1 else "H"
line_re = re.compile(r"^<(f[^.>]+\.[^;>]+);" + re.escape(who) + r">\s+(.*)$")

for raw in open("text16e6.evt", encoding="latin-1"):
    m = line_re.match(raw.rstrip("\n"))
    if not m:
        continue
    locus, text = m.groups()
    text = re.sub(r"\{[^}]*\}", "", text)   # drop inline comments
    text = re.sub(r"[!%]", "", text)        # drop filler/placeholder marks
    text = text.replace("-", "").replace("=", "")  # line/paragraph end marks
    words = [w for w in re.split(r"[.,]+", text) if w]
    if words:
        print(f"{locus}\t{' '.join(words)}")
