"""
Generates index.html from timeline.py + manifest.json.

The output is a single static file with no build step required to deploy —
this script exists so the story stays editable in one place (timeline.py)
instead of being hand-edited HTML. Re-run it after adding a photo.

    python tools/preprocess.py     # convert HEIC / resize / strip EXIF
    python tools/build_site.py     # emit index.html
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))          # timeline.py lives at the repo root

from timeline import CHAPTERS, HERO, CLOSING

OUT = ROOT / "index.html"


def load_dims():
    """filename -> (width, height), so every <img> ships intrinsic size."""
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    return {m["file"]: tuple(map(int, m["dimensions"].split("x"))) for m in manifest}


CSS = """
*,*::before,*::after{box-sizing:border-box}

:root{
  --bg:#0a0e14;
  --bg-soft:#111823;
  --ink:#e9eff7;
  --muted:#93a3b8;
  --blue:#5aa9f0;
  --blue-deep:#2f6fb5;
  --line:rgba(90,169,240,.26);
  --maxw:620px;
}

html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}

body{
  margin:0;
  background:var(--bg);
  color:var(--ink);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:17px;
  line-height:1.65;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
}

/* soft blue wash top and bottom so photos stay the focus */
body::before,body::after{
  content:'';position:fixed;left:0;right:0;height:46vh;
  pointer-events:none;z-index:0;
}
body::before{top:0;background:linear-gradient(180deg,rgba(47,111,181,.30),transparent)}
body::after{bottom:0;background:linear-gradient(0deg,rgba(47,111,181,.26),transparent)}

main{position:relative;z-index:1}

.wrap{width:100%;max-width:var(--maxw);margin:0 auto;padding:0 22px}

/* ---------- hero ---------- */
.hero{
  min-height:92vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;
  padding:18vh 22px 10vh;
}
.eyebrow{
  font-size:11px;letter-spacing:.34em;text-transform:uppercase;
  color:var(--blue);margin:0 0 22px;font-weight:500;
}
.hero h1{
  font-family:'Fraunces',Georgia,serif;
  font-size:clamp(2.5rem,12vw,4.1rem);
  font-weight:600;line-height:1.05;margin:0;
  letter-spacing:-.015em;
  background:linear-gradient(160deg,#ffffff 8%,var(--blue) 92%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.rule{width:52px;height:2px;background:var(--blue);margin:30px auto;border-radius:2px}
.hero .lede{color:var(--muted);max-width:34ch;margin:0 auto;font-size:16px}
.hero .for{color:var(--ink);font-weight:500}
.scroll-cue{
  margin-top:auto;padding-top:12vh;font-size:11px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--muted);
}
.scroll-cue span{display:block;margin-top:10px;font-size:16px;color:var(--blue);animation:drift 2.2s ease-in-out infinite}
@keyframes drift{0%,100%{transform:translateY(0);opacity:.55}50%{transform:translateY(7px);opacity:1}}

/* ---------- chapters ---------- */
.chapter{padding:7vh 0}
.stamp{
  display:flex;align-items:center;gap:12px;margin-bottom:6px;flex-wrap:wrap;
}
.stamp::before{
  content:'';width:6px;height:6px;border-radius:50%;
  background:var(--blue);flex:none;
  box-shadow:0 0 0 4px rgba(90,169,240,.16);
}
.stamp .date{
  font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--blue);font-weight:600;white-space:nowrap;
}
.stamp .place{
  font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);font-weight:400;line-height:1.5;
}
.sub{color:var(--muted);font-size:14.5px;font-style:italic}

figure{margin:24px 0 0}
.frame{
  border-radius:16px;overflow:hidden;background:var(--bg-soft);
  box-shadow:0 18px 44px -18px rgba(0,0,0,.9);
  cursor:zoom-in;
}
.frame img{
  display:block;width:100%;height:auto;
  transition:transform .55s cubic-bezier(.2,.7,.3,1);
}
.frame:hover img{transform:scale(1.02)}

/* framing tweaks */
figure.small .frame{max-width:58%;margin:0 auto}
figure.screenshot .frame{max-width:66%;margin:0 auto;border:1px solid var(--line);border-radius:22px}
figure.wide .frame{border-radius:14px}

figcaption{
  margin-top:18px;color:var(--muted);font-size:15.5px;font-style:italic;
  line-height:1.72;
}

/* ---------- closing ---------- */
/* vertical only -- a `padding` shorthand here would clobber the
   horizontal padding .wrap supplies and run text to the screen edge */
.closing{
  padding-top:22vh;padding-bottom:20vh;text-align:center;
}
.closing h2{
  font-family:'Fraunces',Georgia,serif;
  font-size:clamp(2rem,9vw,3.1rem);font-weight:600;
  line-height:1.12;margin:0 0 26px;letter-spacing:-.01em;
  background:linear-gradient(160deg,#ffffff 10%,var(--blue) 95%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.closing p{color:var(--muted);max-width:36ch;margin:0 auto 34px}
.closing .sign{
  color:var(--ink);font-style:italic;font-size:17px;
  font-family:'Fraunces',Georgia,serif;
}

/* ---------- reveal on scroll ---------- */
.reveal{opacity:0;transform:translateY(26px);transition:opacity .85s ease,transform .85s cubic-bezier(.2,.7,.3,1)}
.reveal.in{opacity:1;transform:none}

/* ---------- lightbox ---------- */
.lightbox{
  position:fixed;inset:0;z-index:50;display:none;
  align-items:center;justify-content:center;padding:20px;
  background:rgba(5,8,12,.96);backdrop-filter:blur(6px);
}
.lightbox.open{display:flex}
.lightbox img{
  max-width:100%;max-height:100%;border-radius:10px;
  box-shadow:0 24px 70px -20px rgba(0,0,0,1);
}
.lightbox button{
  position:absolute;top:16px;right:16px;
  width:44px;height:44px;border-radius:50%;
  background:rgba(255,255,255,.1);border:1px solid var(--line);
  color:#fff;font-size:22px;line-height:1;cursor:pointer;
}
.hint{
  text-align:center;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);padding:14px 22px 0;
}

@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .reveal{opacity:1;transform:none;transition:none}
  .frame img{transition:none}
  .scroll-cue span{animation:none}
}

@media (min-width:760px){
  :root{--maxw:680px}
  .chapter{padding:9vh 0}
}
"""

JS = """
(function () {
  var reveal = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveal.forEach(function (el) { io.observe(el); });
  } else {
    reveal.forEach(function (el) { el.classList.add('in'); });
  }

  var box = document.getElementById('lightbox');
  var big = box.querySelector('img');
  var frames = document.querySelectorAll('.frame');

  function open(src, alt) {
    big.src = src;
    big.alt = alt || '';
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    box.classList.remove('open');
    document.body.style.overflow = '';
  }

  frames.forEach(function (f) {
    f.setAttribute('tabindex', '0');
    f.setAttribute('role', 'button');
    var go = function () {
      var img = f.querySelector('img');
      open(img.getAttribute('src'), img.getAttribute('alt'));
    };
    f.addEventListener('click', go);
    f.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });

  box.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });
})();
"""


# Fold typographic characters to entities so index.html ships as pure ASCII.
# Anything non-ASCII in a static file is one bad editor round-trip away from
# turning into mojibake; entities are unambiguous regardless of charset.
ENTITIES = {
    "\u2014": "&mdash;",   # em dash
    "\u2013": "&ndash;",   # en dash
    "\u2018": "&lsquo;",
    "\u2019": "&rsquo;",
    "\u201c": "&ldquo;",
    "\u201d": "&rdquo;",
    "\u00b7": "&middot;",
    "\u00a9": "&copy;",
}


def esc(s):
    # Escape the five ASCII specials FIRST, then fold the remaining
    # typographic characters to entities. Doing it in the other order would
    # double-escape the entity we just introduced (& -> &amp;).
    s = html.escape(s, quote=True)
    for ch, ent in ENTITIES.items():
        s = s.replace(ch, ent)
    return s


def build_chapter(ch, dims):
    w, h = dims.get(ch["file"], (900, 1200))
    mods = ch.get("mods")
    cls = f' class="{mods}"' if mods else ""
    # compose first, then escape the whole thing -- otherwise a literal
    # separator here would smuggle non-ASCII past esc()
    alt = f'{ch["sub"]} \u2014 {ch["stamp"]}'
    return f"""    <section class="chapter reveal">
      <div class="stamp">
        <span class="date">{esc(ch["stamp"])}</span>
        <span class="place">{esc(ch["sub"])}</span>
      </div>
      <figure{cls}>
        <div class="frame">
          <img src="{esc(ch["file"])}" alt="{esc(alt)}"
               width="{w}" height="{h}" loading="lazy" decoding="async">
        </div>
        <figcaption>{esc(ch["caption"])}</figcaption>
      </figure>
    </section>"""


def main():
    dims = load_dims()

    missing = [c["file"] for c in CHAPTERS if not (ROOT / c["file"]).exists()]
    if missing:
        raise SystemExit("Missing photo(s):\n  " + "\n  ".join(missing))

    chapters = "\n".join(build_chapter(c, dims) for c in CHAPTERS)

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>To My Babyyyy &middot; Andria</title>
<meta name="description" content="Every photo I kept, in the order they happened.">
<meta name="theme-color" content="#0a0e14">
<meta property="og:title" content="To My Babyyyy">
<meta property="og:description" content="Every photo I kept, in the order they happened.">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ctext y='26' font-size='26'%3E%F0%9F%92%97%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<main>

  <header class="hero reveal">
    <p class="eyebrow">{esc(HERO["title"])}</p>
    <h1>To My<br>Babyyyy</h1>
    <div class="rule"></div>
    <p class="lede">{esc(HERO["lede"])}<br>For <span class="for">{esc(HERO["name"])}</span>.</p>
    <p class="scroll-cue">Scroll<span>&darr;</span></p>
  </header>

  <div class="wrap">
{chapters}
  </div>

  <footer class="closing wrap reveal">
    <h2>{esc(CLOSING["title"])}</h2>
    <p>{esc(CLOSING["body"])}</p>
    <p class="sign">{esc(CLOSING["sign"])}</p>
  </footer>

</main>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo">
  <button type="button" aria-label="Close">&times;</button>
  <img alt="">
</div>

<script>{JS}</script>
</body>
</html>
"""

    OUT.write_text(doc, encoding="utf-8")
    print(f"  wrote {OUT.relative_to(ROOT)}  ({len(doc) / 1024:.1f} KB, {len(CHAPTERS)} chapters)")


if __name__ == "__main__":
    main()