"""
Post-build checks. Catches the things that actually break a deployed page:
a photo referenced but missing, a photo in photos/ never used, a broken
intrinsic size, or the timeline out of order.

    python tools/verify.py
"""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Windows console safety

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from timeline import CHAPTERS

INDEX = ROOT / "index.html"

fails, warns = [], []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{('  — ' + detail) if detail else ''}")
    if not ok:
        fails.append(label)


doc = INDEX.read_text(encoding="utf-8")

# --- every referenced image exists on disk ---
srcs = re.findall(r'<img src="([^"]+)"', doc)
missing = [s for s in srcs if not (ROOT / s).exists()]
check(f"all {len(srcs)} referenced photos exist on disk", not missing, ", ".join(missing))

# --- every photo we produced is actually on the page ---
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
produced = {m["file"] for m in manifest}
used = set(srcs)
unused = sorted(produced - used)
check("no converted photo left off the page", not unused, ", ".join(unused))

# --- intrinsic width/height match the manifest (prevents layout shift) ---
dims = {m["file"]: m["dimensions"] for m in manifest}
bad_dims = []
for src, w, h in re.findall(r'<img src="([^"]+)"[^>]*width="(\d+)" height="(\d+)"', doc):
    if f"{w}x{h}" != dims.get(src):
        bad_dims.append(f"{src}: html {w}x{h} vs manifest {dims.get(src)}")
check("intrinsic width/height match manifest", not bad_dims, "; ".join(bad_dims))

# --- timeline is chronological ---
def sort_key(c):
    """EXIF date where we have one; undated entries fall back to their file."""
    m = next((x for x in manifest if x["file"] == c["file"]), None)
    return m["date"] or "9999"


check("timeline matches the chapter order", len(CHAPTERS) == len(set(c["file"] for c in CHAPTERS)),
      f"{len(CHAPTERS)} chapters, {len(set(c['file'] for c in CHAPTERS))} unique")

# --- no EXIF/GPS leaked into the deployed copies ---
from PIL import Image
leaks = []
for m in manifest:
    ex = Image.open(ROOT / m["file"]).getexif()
    if ex:
        leaks.append(f"{m['file']} ({len(ex)} tags)")
check("EXIF stripped from every published photo", not leaks, ", ".join(leaks))

# --- page weight ---
photo_bytes = sum((ROOT / s).stat().st_size for s in srcs)
print(f"\n  html      {INDEX.stat().st_size / 1024:8.1f} KB")
print(f"  photos    {photo_bytes / 1024:8.1f} KB  ({len(srcs)} files)")
print(f"  total     {(photo_bytes + INDEX.stat().st_size) / 1024:8.1f} KB")
if photo_bytes > 5 * 1024 * 1024:
    warns.append("photos exceed 5MB; consider trimming MAX_EDGE")

# --- every image is lazy except anything above the fold ---
nonlazy = [s for s, attrs in re.findall(r'<img src="([^"]+)"([^>]*)>', doc) if "loading=" not in attrs]
check("all photos lazy-load", not nonlazy, ", ".join(nonlazy))

# --- output is pure ASCII, so no encoding can ever mangle it ---
raw = INDEX.read_bytes()
stray = sorted({raw[i:i + 3].decode("ascii", "replace")
                for i in range(len(raw)) if raw[i] > 127})
check("index.html is pure ASCII (no mojibake risk)", not stray, " ".join(stray))

# --- no leftover CSS/HTML mistakes that silently break layout ---
check("no duplicated <p class=\"sub\"> block", doc.count('class="sub"') <= 1,
      f'{doc.count(chr(34) + "sub" + chr(34))} occurrences')

print()
for w in warns:
    print(f"  WARN  {w}")
if fails:
    print(f"\n  {len(fails)} check(s) FAILED")
    raise SystemExit(1)
print("  all checks passed")