#!/usr/bin/env python3
"""Generate palette/style variants: index.html (live), plum/, and archive/<slug>/.

Single source of truth = template.html. Each theme below only overrides the CSS
:root color variables (and optionally a little extra CSS for a distinct feel),
so the content never forks. Re-run this whenever template.html changes.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = (ROOT / "template.html").read_text(encoding="utf-8")

# name, slug, blurb, palette vars, extra css for a slightly different feel
THEMES = [
    {
        "slug": "heritage",
        "name": "Heritage Green",
        "blurb": "Deep forest green and gold. Established, warm, trustworthy — the current look.",
        "vars": dict(navy="13323d", navy_deep="0c1a20", green="2f6b4f", green_dk="244f3b",
                     gold="c2913a", gold_lt="e0c789", gold_deep="7f5e17", cream="faf6ee", paper="fffdf9",
                     ink="1d2a2d", muted="5d6e72", line="e8e1d2"),
        "css": "",
    },
    {
        "slug": "plum",
        "name": "Royal Plum",
        "blurb": "Rich aubergine purple and gold — matches the new reference image. Elegant, premium, dignified.",
        # gold brightened out of mustard: same ~38° hue, higher value + saturation so it
        # reads as gold rather than brown. gold_deep still passes WCAG AA (~5.3:1) on
        # both cream and paper for small text on light bands.
        # The green slots used to hold more purple, leaving the page one hue plus gold.
        # They now hold a muted sage — warm rather than clinical, and drawn from the leaves
        # in the logo mark. green_dk passes WCAG AA (~5.9:1) on paper for small text.
        # cream shifted off lilac to a warm sage-grey so light bands read apart from paper.
        "vars": dict(navy="3a2150", navy_deep="241033", green="7d9573", green_dk="4e6a48",
                     gold="e8b23e", gold_lt="f2dca8", gold_deep="8a5a0a", cream="eef1ea", paper="fffdfb",
                     ink="2a1c33", muted="6c5d75", line="e1e7db"),
        "css": ".btn{border-radius:999px}.card{border-radius:18px}"
               ".mvcard,.val,.stat{border-radius:16px}",
    },
    {
        "slug": "slate",
        "name": "Slate Blue",
        "blurb": "Calm healthcare blue with warm gold. Clinical, reassuring, professional.",
        "vars": dict(navy="1f3a5c", navy_deep="122438", green="2f8296", green_dk="1f6274",
                     gold="cda24a", gold_lt="ecd49a", gold_deep="7a5f18", cream="f3f6f9", paper="ffffff",
                     ink="16283b", muted="566778", line="dde5ec"),
        "css": ".card{border-radius:12px}.btn{border-radius:6px}",
    },
    {
        "slug": "clay",
        "name": "Warm Clay",
        "blurb": "Terracotta and cocoa over cream. Warm, earthy, human — the most distinct of the set.",
        "vars": dict(navy="6b3b2e", navy_deep="47241b", green="6e7d3f", green_dk="55632f",
                     gold="c8743f", gold_lt="e6a368", gold_deep="9a4f22", cream="f7efe4", paper="fffdf8",
                     ink="33271f", muted="6e5f52", line="ecdfcf"),
        "css": ".btn{border-radius:999px}.card{border-radius:16px}"
               ".eyebrow{letter-spacing:.2em}h1,h2,h3{letter-spacing:-.015em}",
    },
]

ROOT_TMPL = """:root{{
    --navy:#{navy}; --navy-deep:#{navy_deep}; --green:#{green}; --green-dk:#{green_dk};
    --gold:#{gold}; --gold-lt:#{gold_lt}; --gold-deep:#{gold_deep}; --cream:#{cream}; --paper:#{paper};
    --ink:#{ink}; --muted:#{muted}; --line:#{line};
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }}"""

# Rebecca picked Royal Plum (2026-07) — it builds as the live site (index.html).
# The other looks are kept buildable but archived under archive/<slug>/.
# Each non-live look is written as <dir>/index.html so it gets a clean URL
# (/plum, /archive/heritage, …) on any static host — no rewrite config needed.
DEFAULT_SLUG = "plum"
ARCHIVE = ROOT / "archive"

BANNER = """<div style="background:#11181b;color:#e7d9b6;font:600 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:10px 16px;display:flex;justify-content:center;gap:16px;align-items:center;border-bottom:1px solid rgba(255,255,255,.08)">
  <span>Archived look: <b style="color:#fff">{name}</b></span>
  <a href="/" style="color:#e0c789;text-decoration:none">&larr; Live site</a>
</div>"""

def render(t, asset_prefix, banner):
    html = SRC
    new_root = ROOT_TMPL.format(**t["vars"])
    html = re.sub(r":root\{.*?\}", new_root, html, count=1, flags=re.DOTALL)
    html = re.sub(r'(<meta name="theme-color" content=")#[0-9a-fA-F]{3,6}(">)',
                  rf'\g<1>#{t["vars"]["navy_deep"]}\g<2>', html)
    if t["css"]:
        html = html.replace("</style>", f"\n  /* {t['name']} tweaks */\n  {t['css']}\n</style>", 1)
    if asset_prefix:
        html = html.replace('src="assets/', f'src="{asset_prefix}assets/')
        html = html.replace('href="assets/', f'href="{asset_prefix}assets/')
    if banner:
        html = html.replace("<body>\n", "<body>\n" + BANNER.format(name=t["name"]) + "\n", 1)
    return html

for t in THEMES:
    if t["slug"] == DEFAULT_SLUG:
        (ROOT / "index.html").write_text(render(t, "", banner=False), encoding="utf-8")
        print("wrote index.html (live site — Royal Plum)")
        # keep /plum serving the same page (Rebecca's review link)
        d = ROOT / t["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render(t, "../", banner=False), encoding="utf-8")
        print(f"wrote {t['slug']}/index.html  -> /{t['slug']}")
    else:
        d = ARCHIVE / t["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render(t, "../../", banner=True), encoding="utf-8")
        print(f"wrote archive/{t['slug']}/index.html  -> /archive/{t['slug']} (archived)")
