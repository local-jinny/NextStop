#!/usr/bin/env python3
"""data/posters.json + template/*.html -> gallery.html, poster/01.html..12.html
콘텐츠(제목/작가/설명 등)를 바꾸려면 data/posters.json만 수정하고 이 스크립트를 다시 실행하세요.
index.html(랜딩 페이지)은 정적 파일이라 이 스크립트가 건드리지 않습니다.
    python3 scripts/build.py
"""
import json
import os
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sns_handle(url):
    """https://instagram.com/artist_handle -> @artist_handle"""
    path = urlparse(url).path.strip("/")
    handle = path.split("/")[0] if path else url
    return f"@{handle}"

with open(os.path.join(ROOT, "data", "posters.json"), encoding="utf-8") as f:
    posters = json.load(f)

with open(os.path.join(ROOT, "template", "poster.template.html"), encoding="utf-8") as f:
    poster_tpl = f.read()

with open(os.path.join(ROOT, "template", "gallery.template.html"), encoding="utf-8") as f:
    gallery_tpl = f.read()

n = len(posters)

# ---- poster/XX.html 생성 ----
for i, p in enumerate(posters):
    prev_p = posters[(i - 1) % n]
    next_p = posters[(i + 1) % n]

    html = poster_tpl
    for key, val in [
        ("ID", p["id"]),
        ("TITLE_KO", p["title_ko"]),
        ("TITLE_EN", p["title_en"]),
        ("ARTIST", p["artist"]),
        ("SNS", p["sns"]),
        ("SNS_HANDLE", sns_handle(p["sns"])),
        ("DESC", p["desc"]),
        ("IMAGE", p["image"]),
        ("PREV_HREF", f"{prev_p['id']}.html"),
        ("PREV_TITLE", prev_p["title_ko"]),
        ("NEXT_HREF", f"{next_p['id']}.html"),
        ("NEXT_TITLE", next_p["title_ko"]),
    ]:
        html = html.replace("{{" + key + "}}", val)

    out_path = os.path.join(ROOT, "poster", f"{p['id']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"generated poster/{p['id']}.html")

# ---- gallery.html 생성 ----
cards = []
for p in posters:
    cards.append(f'''      <a class="poster-card" href="poster/{p['id']}.html">
        <div class="thumb">
          <img src="assets/images/{p['image']}" alt="{p['title_ko']}"
               onerror="this.remove()">
        </div>
        <div class="meta">
          <div class="num">NO. {p['id']}</div>
          <h3>{p['title_ko']}</h3>
          <div class="artist">{p['artist']}</div>
        </div>
      </a>''')

gallery_html = gallery_tpl.replace("{{CARDS}}", "\n".join(cards))
with open(os.path.join(ROOT, "gallery.html"), "w", encoding="utf-8") as f:
    f.write(gallery_html)
print("generated gallery.html")
