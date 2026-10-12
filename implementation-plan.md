# Anniversary Website — Implementation Plan

**Project:** Scrolling Love Story — a single-page website that tells your relationship story through photos and a few honest lines.  
**Deploy:** GitHub Pages (free), link sent to her phone.  
**Author:** [Your name]  
**Date:** October 12, 2026  

---

## 1. Concept

A single vertical page. She opens the link on her phone, and as she scrolls, your relationship unfolds through photos arranged chronologically. Each photo is a "chapter" — anchored by its real date (from EXIF) and a short caption. The scroll ends on something present-day: the anniversary itself, or what you're looking forward to.

**Tone:** Intimate, sincere, not over-produced. The photos do the heavy lifting. The words are light but real.

**Design:** Minimal, warm, readable on a phone screen. Dark or soft neutral background so photos stand out. Typography that feels hand-picked, not default.

---

## 2. Photo Inventory (from EXIF + file analysis)

**17 photos total.** Spanning 12+ years (2014–2026).

### Photos WITH EXIF dates (ordered chronologically):

| Date | File | Device | GPS | Notes |
|------|------|--------|-----|-------|
| 2014-04-20 | `IMG_5516 (1).JPG` | Canon PowerShot D30 | — | 480×480, 55KB — old, small |
| 2025-04-22 | `IMG_5710 (1).JPG` | iPhone 13 | 7.0783°N, 125.6135°E | 1536×2048, 720KB |
| 2025-04-28 | `IMG_0122 (1).JPG` | iPhone 13 | 7.0726°N, 125.6121°E | 1536×2048, 870KB |
| 2025-05-29 | `IMG_0274 (1).JPG` | iPhone 13 | 7.0737°N, 125.6125°E | 1536×2048, 809KB |
| 2025-12-13 | `IMG_6456.JPG` | iPhone X | 7.0792°N, 125.6131°E | 4032×3024, 3070KB |
| 2026-04-15 | `IMG_8123 (1).JPG` | iPhone X | 7.0723°N, 125.6146°E | 4032×3024, 2448KB |
| 2026-06-28 | `IMG_8953 (1).JPG` | iPhone X | 7.5387°N, 125.9177°E | 3088×2320, 1053KB |
| 2026-08-29 | `IMG_9467.JPG` | iPhone X | 7.0781°N, 125.6138°E | 4032×3024, 2900KB |
| ~2025-06-16 | `IMG_3010.PNG` | — | — | 1125×2436, 6713KB — likely a screenshot or screen capture |

### Photos WITHOUT EXIF dates (order by visual analysis / filename hints):

| File | Size | Notes |
|------|------|-------|
| `IMG_1237 (1).HEIC` | 236KB | HEIC — needs conversion |
| `IMG_3460 (1).HEIC` | 1152KB | HEIC — needs conversion |
| `IMG_3674.HEIC` | 1352KB | HEIC — needs conversion |
| `IMG_9039.HEIC` | 1950KB | HEIC — needs conversion |
| `Messenger_creation_C15819A6-DECA-482B-9DE3-74C2B37F10F2 (1).JPEG` | 123KB | From Messenger — likely a chat screenshot or forwarded image |
| `att.ZBk4kn5ftOnaU09-TisvBuLaqDEdUvOXNC8P5KT3sso.JPG` | 1250KB | "att" prefix — attachment, possibly from a message |
| `att.aRLKyR59xkpQtmliKSBAbnjFl0asNZ470gqcJ5R01so (1).JPG` | 321KB | "att" prefix — attachment |
| `att.guzY0FsyQaNhV9_Cra_XGGj9BFtvLVD7fF7mJnzu6t4 (1).JPG` | 592KB | "att" prefix — attachment |

### Key observations:
- **GPS cluster:** Most dated photos are around 7.07–7.08°N, 125.61°E — same general location (looks like Davao/Mindanao area). This suggests a recurring place in your relationship.
- **Device evolution:** iPhone 13 (2025) → iPhone X (2026). Implies these are from different periods.
- **HEIC files:** 4 photos in HEIC format. These need to be converted to JPEG or WebP before the website can display them in a browser.
- **"att" files:** Likely received via Messenger or email — attachments. The "guzY0Fs" one is high-res (3024×4032) — possibly a meaningful photo sent to you.
- **Messenger file:** `Messenger_creation_C15819A6...` — clearly a Messenger-generated image. Could be a chat screenshot, a sticker, or a photo shared through Messenger.

---

## 3. What the Coding Agent Must Do

### A. Photo preprocessing

1. **Convert HEIC → JPEG/WebP.** Use a tool like `ffmpeg` (libheif), `heif-convert`, or Python's `pyheif` + PIL. Output converted files alongside originals (e.g., `IMG_1237 (1).webp`).
2. **Optimize large files.** `IMG_3010.PNG` is 6.7MB — resize or compress for web. Photos over 2MB should be downsampled to a max width of ~1200px for phone viewing.
3. **Handle the Messenger and "att" files** — these may need visual analysis to determine what they are and where they fit in the story.

### B. Visual analysis (vision)

The coding agent MUST analyze each photo visually. For each photo, produce:

- A **one-line description** of what's in the photo (setting, people, activity, mood)
- A **suggested caption** — 1-2 sentences max, in your voice. The agent should write these as if *you* are speaking to *her*. Not generic. Not AI-polished. Real.
- A **suggested placement** in the timeline — use the EXIF date when available; for undated photos, place them where the visual content suggests they belong.

**Caption style guide for the agent:**
- Short. 1-2 sentences. Sometimes just a date + location is enough.
- Honest, specific, personal. References to real moments.
- From your perspective ("I remember...", "This was the day...", "You were...").
- Not over-written. No purple prose.
- Vary the tone: some captions can be warm, some funny, some quiet.

### C. Build the website

**Tech stack:** Single HTML file + embedded CSS + optional small JS. No framework. No build step. Deploy directly to GitHub Pages.

**Structure:**

```
/ (root)
├── index.html          # Single-page website
├── photos/             # All photos (originals + converted)
│   ├── IMG_5516 (1).JPG
│   ├── IMG_5516 (1).webp        # converted from HEIC
│   ├── ...
│   └── converted/               # converted HEIC files
├── assets/             # Optional: favicon, fonts
└── README.md           # Optional
```

**Page layout:**

1. **Opening:** Header reading **"To My Babyyyy"** in a warm, affectionate style. Accent color: **blue** — both of your favorite color. Use it sparingly (headings, dividers, hover states, a subtle gradient) so it doesn't overwhelm the photos. Let the first photo hit soon after.
2. **Photo chapters (scrollable):** Each chapter = date header + photo + caption. Stacked vertically. As she scrolls, the story moves forward.
3. **Spacing:** Generous whitespace between chapters so it breathes on a phone screen. Photos centered, max-width for large screens.
4. **Ending:** A final section built around *"It's us against the world"* — the two of you, together, facing whatever comes next. This is the landing moment. Use Andria's name somewhere in the opening or closing.

**Visual design direction:**
- **Color palette:** Blue as the accent — both of your favorite color. Background stays neutral (soft cream/off-white or deep charcoal) so blue pops and photos stay the focus. Blue for the "To My Babyyyy" header, captions' date stamps, dividers, link/hover states, and a subtle blue-tinted gradient at the top or bottom of the page.
- Soft, warm background (off-white, cream, or deep dark — pick one that makes photos pop)
- Clean sans-serif for body text
- Photo captions in a lighter weight, smaller size, maybe italic
- Subtle transitions? Optional — a fade-in as photos enter viewport could feel nice but isn't required
- Mobile-first: test on a phone screen size (375px wide)

**Interactive consideration (optional, only if time permits):**
- A "click to expand" on photos for full-screen view
- A subtle parallax or fade effect on scroll (lightweight, CSS-only if possible)
- A final "reveal" — last section hidden until she reaches it

---

## 4. EXIF Data Reference (for the agent)

The agent should use EXIF dates as the primary timeline anchor. Here's the ordered list:

```
2014-04-20 → IMG_5516 (1).JPG (Canon — oldest)
2025-04-22 → IMG_5710 (1).JPG (iPhone 13, GPS: 7.0783, 125.6135)
2025-04-28 → IMG_0122 (1).JPG (iPhone 13, GPS: 7.0726, 125.6121)
2025-05-29 → IMG_0274 (1).JPG (iPhone 13, GPS: 7.0737, 125.6125)
2025-06-16 → IMG_3010.PNG (no device info — likely screenshot)
2025-12-13 → IMG_6456.JPG (iPhone X, GPS: 7.0792, 125.6131)
2026-04-15 → IMG_8123 (1).JPG (iPhone X, GPS: 7.0723, 125.6146)
2026-06-28 → IMG_8953 (1).JPG (iPhone X, GPS: 7.5387, 125.9177)
2026-08-29 → IMG_9467.JPG (iPhone X, GPS: 7.0781, 125.6138)
```

**Undated photos:** Place using visual analysis. The "att" files and Messenger file likely came from messages — they may represent a specific moment in your communication. Use the visual content + filename hints to place them.

---

## 5. Deployment

1. Create a GitHub repo (public or private — public is easier for GitHub Pages).
2. Push the `index.html` + `photos/` folder.
3. Enable GitHub Pages in repo settings (source: main branch, `/root` folder).
4. Get the URL → send it to her.

**Repo name suggestion:** Something she'd recognize or find curious. Not "anniversary-website" — that's too obvious before she opens it. Maybe your name + her name, or something abstract. Or just `username.github.io/anniversary` if you want it clean.

---

## 6. Timeline (1 hour)

| Time | Task |
|------|------|
| 0:00–0:10 | HEIC conversion + photo optimization |
| 0:10–0:30 | Visual analysis of all 17 photos + caption writing |
| 0:30–0:50 | Build the HTML/CSS page with all photos and captions |
| 0:50–0:55 | Test on phone-sized viewport, fix layout issues |
| 0:55–1:00 | Push to GitHub, enable Pages, verify URL works |

This is tight. If the agent hits a snag, pare down: fewer photos (the 9 dated ones are the spine), simpler layout, no fancy effects.

---

## 7. Edge Cases & Risks

- **HEIC compatibility:** Browsers don't display HEIC. Must convert. If conversion fails, drop those 4 photos from the timeline rather than block the build.
- **Large PNG:** `IMG_3010.PNG` at 6.7MB will slow page load on mobile data. Compress or exclude.
- **GPS privacy:** The EXIF data contains GPS coordinates. If you're uncomfortable with these being embedded in the deployed site, strip EXIF from the placed images (the website itself doesn't need to expose this — just use the data to order the timeline).
- **Missing captions:** If the agent can't determine what a photo is, use the date + location only, or place it as a "memory" without a caption.
- **Phone rendering:** Test on actual phone or phone-sized viewport. Photos should not overflow, text should be readable without zooming.

---

## 8. What You (the Human) Should Provide

- **Your voice:** The agent will draft captions, but you should review them. It's your story — the words should sound like you. Quick edits are fine.
- **A final line:** What do you want her to read at the end? A confession, a hope, a memory? Give the agent 1-2 sentences for the closing section.
- **Her name:** Andria Faith P. Rodio — use in the opening/header. Tone can be affectionate ("My Babyyyy" energy) but the page itself stays sincere and grounded.
- **A final line:** "It's us against the world" — this is the closing sentiment. The last section should land on this idea: the two of you, together, facing whatever comes next.

---

## 9. Deliverable

A GitHub Pages URL that, when opened on her phone, shows a scrolling love story: your photos in chronological order, each with a date and a real caption, ending on the present moment.

---

*Plan prepared for the coding agent. EXIF data extracted on October 12, 2026. Photos located at `E:\Projects\Anniversary\`.*
