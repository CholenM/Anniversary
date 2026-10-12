# To My Babyyyy

A single scrolling page that tells one relationship story through 17 photos,
in the order they happened. Built for GitHub Pages, meant to be opened on a phone.

---

## What's here

```
index.html          the whole site - one self-contained file
photos/             the 17 photos, converted, resized, EXIF-stripped
timeline.py         the story: order, date labels, captions  <- EDIT THIS
tools/preprocess.py converts the originals into photos/
tools/build_site.py renders timeline.py -> index.html
tools/verify.py     post-build checks
manifest.json       generated record of every photo (date, size, device)
```

Deploying needs `index.html` and `photos/`. Nothing else is served.

## Editing the captions

`timeline.py` is the only file worth touching. Each entry is:

```python
{
    "file": "photos/img_8953-1.jpg",
    "stamp": "June 28, 2026",      # the date line
    "sub": "At home",               # the small label beside it
    "caption": "No lanyards. ...",  # what she reads
    "mods": "wide",                 # optional framing tweak
}
```

Then re-render and check:

```
python tools/build_site.py
python tools/verify.py
```

`mods` is optional and only affects presentation:
`small` (low-res source, don't blow it up), `screenshot` (phone screenshot,
give it a device frame), `wide` (landscape shot).

## Regenerating the photos

Only needed if you change the source images or `MAX_EDGE`:

```
pip install pillow pillow_heif
python tools/preprocess.py
python tools/build_site.py
```

This converts the 4 HEIC files (browsers can't display them), downscales
anything over 1200px, and **strips all EXIF including GPS coordinates** before
writing to `photos/`. The originals at the repo root are never modified and are
excluded by `.gitignore`.

## Deploying to GitHub Pages

1. Create a repository (public, so Pages works on the free tier).
2. Push this folder.
3. **Settings -> Pages -> Source: Deploy from a branch**, pick your branch
   and `/ (root)`.
4. Your URL is `https://<user>.github.io/<repo>/` and shows up ~1 min later.

> This repo's branch is `master`. If you rename it to `main`, pick `main` in
> the Pages source dropdown.

Open the URL on your phone before sending it — that's the real test.

## Notes on what was decided

- **Timeline.** Dated photos are ordered by their EXIF date. Three photos the
  original plan listed as undated turned out to *have* dates once converted
  (2025-07-04, 2025-11-19, 2026-08-29), so they're anchored properly. The four
  genuinely undated ones are labelled honestly ("A night, date unknown") rather
  than given an invented date.
- **`IMG_1237 (1).HEIC`** was stored rotated with no EXIF orientation tag, so
  the normal rotation fix couldn't catch it. It's corrected by hand in
  `MANUAL_ROTATE`.
- **GPS.** The originals carry location data. It's used to sanity-check the
  timeline and then removed from every published image.
- **Page weight.** 25 MB of originals became ~2.4 MB of photos, plus an 18 KB
  HTML file. Everything lazy-loads, so she doesn't download the whole story
  before the first photo appears.
- **Typography** loads from Google Fonts; the page falls back to system fonts
  offline and still reads fine.