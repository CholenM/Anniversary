"""
Photo preprocessing for the Anniversary site.

- HEIC -> JPEG (browsers can't render HEIC)
- Downsample anything wider than MAX_EDGE to MAX_EDGE px
- Re-encode as progressive JPEG, quality 82
- STRIP all EXIF (including GPS) from the deployed copies (privacy, per plan sec. 7)
- Write a manifest.json with the original EXIF date/device/gps for timeline ordering

Originals are never modified; everything lands in photos/.
"""

import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "photos"
MAX_EDGE = 1200          # plan: max width ~1200px for phone viewing
JPEG_QUALITY = 82
SUPPORTED = {".jpg", ".jpeg", ".png", ".heic"}

# Files whose pixels are rotated but that carry no EXIF orientation tag, so
# exif_transpose() can't fix them. Value = degrees clockwise to correct.
MANUAL_ROTATE = {
    "IMG_1237 (1).HEIC": 270,   # shot sideways; heads point left in the raw file
}


def slugify(name: str) -> str:
    """Stable, URL-safe filename. Keeps original stem, drops the extension."""
    stem = Path(name).stem
    out = []
    for ch in stem:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch in " ()":
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-").lower()


def read_exif_date(img: Image.Image):
    """Pull DateTimeOriginal / DateTimeDigitized. Returns (iso_date|None, device|None, gps|None)."""
    try:
        exif = img.getexif()
    except Exception:
        return None, None, None
    if not exif:
        return None, None, None

    date = None
    # 36867 = DateTimeOriginal, 36868 = DateTimeDigitized
    for tag in (36867, 36868, 306):
        raw = exif.get(tag)
        if raw:
            try:
                date = str(raw)[:10]  # YYYY:MM:DD
                date = f"{date[0:4]}-{date[5:7]}-{date[8:10]}"
                break
            except Exception:
                continue

    device = None
    make = exif.get(271)
    model = exif.get(272)
    if make or model:
        device = " ".join(str(p) for p in (make, model) if p).strip() or None

    # GPS (tag 34853 block) -- used only for timeline hints, never written out
    gps = None
    try:
        if 34853 in exif:
            g = exif.get_ifd(34853)
            if 2 in g and 4 in g:
                lat = float(g[2]); lon = float(g[4])
                gps = [round(lat, 4), round(lon, 4)]
    except Exception:
        gps = None

    return date, device, gps


def main() -> int:
    if not OUT_DIR.exists():
        OUT_DIR.mkdir(parents=True)

    sources = sorted(
        p for p in ROOT.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
    if not sources:
        print("No source images found.", file=sys.stderr)
        return 1

    manifest = []
    for src in sources:
        before_kb = src.stat().st_size / 1024
        try:
            img = Image.open(src)
            img.load()
        except Exception as exc:
            print(f"  SKIP  {src.name}: unreadable ({exc})")
            continue

        date, device, gps = read_exif_date(img)

        # Honour EXIF orientation, then bake it in so we can safely drop EXIF.
        img = ImageOps.exif_transpose(img)
        if src.name in MANUAL_ROTATE:
            img = img.rotate(-MANUAL_ROTATE[src.name], expand=True)

        # Flatten alpha (the PNG screenshot) onto white.
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        w, h = img.size
        if max(w, h) > MAX_EDGE:
            img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        out_w, out_h = img.size

        slug = slugify(src.name)
        dest = OUT_DIR / f"{slug}.jpg"
        # No exif= arg -> PIL writes no EXIF block at all (GPS stripped).
        img.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)

        after_kb = dest.stat().st_size / 1024
        manifest.append({
            "src": src.name,
            "file": f"photos/{slug}.jpg",
            "orig_size": src.stat().st_size,
            "bytes": dest.stat().st_size,
            "orig_dimensions": f"{w}x{h}",
            "dimensions": f"{out_w}x{out_h}",
            "date": date,
            "device": device,
            "gps": gps,
        })
        flag = "HEIC" if src.suffix.lower() == ".heic" else "    "
        print(
            f"  OK    [{flag}] {src.name[:44]:<44} "
            f"{w}x{h} -> {out_w}x{out_h}  "
            f"{before_kb:7.0f}KB -> {after_kb:6.0f}KB  date={date or '-'}"
        )

    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    total_before = sum(m["orig_size"] for m in manifest)
    total_after = sum(m["bytes"] for m in manifest)
    print(
        f"\n  {len(manifest)} photos  |  "
        f"{total_before/1024/1024:.1f}MB -> {total_after/1024/1024:.1f}MB  "
        f"({100 - total_after*100//total_before}% smaller)"
    )
    print(f"  manifest -> {ROOT / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())