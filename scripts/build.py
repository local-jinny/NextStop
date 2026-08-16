#!/usr/bin/env python3
"""data/posters.json + template/*.html -> gallery.html, poster/01.html..NN.html
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


def sns_block(p):
    """SNS 주소가 없으면 빈 문자열(링크 자체를 숨김).
    sns_list(계정 여러 개)가 있으면 각각 별도의 <a> 링크로, 없으면 sns 단일 주소로 <a> 하나를 반환."""
    multi = p.get("sns_list")
    if multi:
        links = [
            f'<a class="sns" href="{item["url"]}" target="_blank" rel="noopener">{item["label"]}</a>'
            for item in multi
        ]
        return ", ".join(links)
    url = p.get("sns", "").strip()
    if not url:
        return ""
    label = p.get("sns_label") or sns_handle(url)
    return f'<a class="sns" href="{url}" target="_blank" rel="noopener">{label}</a>'


def img_with_placeholder(src, alt, placeholder_text):
    """onerror 시 이미지를 줄무늬 placeholder-box로 교체하는 <img> 태그.
    JS 객체 리터럴({...})이 섞여 있어 f-string 대신 문자열 결합으로 조립한다."""
    return (
        '<img src="../assets/images/' + src + '" alt="' + alt + '" loading="lazy"\n'
        "             onerror=\"this.replaceWith(Object.assign(document.createElement('div'),"
        "{className:'placeholder-box',innerHTML:'" + placeholder_text + "'}))\">"
    )


def detail_image_block(p):
    """포스터 상세페이지 좌측 이미지 영역. extra_images가 있으면(04/06/08 등)
    메인 포스터 + 상세컷을 한 슬라이더로, 없으면 기존처럼 이미지 1장만 렌더링한다.
    video가 있으면(08 등) 1번 슬라이드를 이미지 대신 영상으로 대체한다."""
    extra = p.get("extra_images") or []
    video = p.get("video")

    if not extra and not video:
        return "        " + img_with_placeholder(
            p["image"], p["title_ko"], "이미지 준비 중<br>" + p["id"] + " / " + p["image"]
        )

    slides = []
    if video:
        slides.append(
            '          <div class="poster-slider-slide">\n'
            '            <video src="../assets/images/' + video + '" '
            'poster="../assets/images/' + p["image"] + '" '
            'autoplay muted loop playsinline preload="metadata"></video>\n'
            "          </div>"
        )
        for idx, src in enumerate(extra, start=1):
            alt = p["title_ko"] + " 상세컷 " + str(idx)
            placeholder = "상세컷 " + str(idx) + " 준비 중<br>" + src
            slides.append(
                '          <div class="poster-slider-slide">\n'
                "            " + img_with_placeholder(src, alt, placeholder) + "\n"
                "          </div>"
            )
        total = 1 + len(extra)
    else:
        all_images = [p["image"]] + extra
        for idx, src in enumerate(all_images, start=1):
            if idx == 1:
                alt = p["title_ko"]
                placeholder = "이미지 준비 중<br>" + p["id"] + " / " + src
            else:
                alt = p["title_ko"] + " 상세컷 " + str(idx - 1)
                placeholder = "상세컷 " + str(idx - 1) + " 준비 중<br>" + src
            slides.append(
                '          <div class="poster-slider-slide">\n'
                "            " + img_with_placeholder(src, alt, placeholder) + "\n"
                "          </div>"
            )
        total = len(all_images)

    dots = [
        '          <button class="poster-slider-dot'
        + (" is-active" if i == 0 else "")
        + '" type="button" aria-label="'
        + str(i + 1)
        + "번째 " + ("영상" if (video and i == 0) else "이미지") + "\"></button>"
        for i in range(total)
    ]

    return (
        '        <div class="poster-slider" data-slider>\n'
        '          <div class="poster-slider-viewport">\n'
        '            <div class="poster-slider-track" data-slider-track>\n'
        + "\n".join(slides) + "\n"
        "            </div>\n"
        '            <button class="poster-slider-arrow prev" type="button" data-slider-prev aria-label="이전 이미지">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 6 9 12 15 18"></polyline></svg></button>\n'
        '            <button class="poster-slider-arrow next" type="button" data-slider-next aria-label="다음 이미지">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 6 15 12 9 18"></polyline></svg></button>\n'
        "          </div>\n"
        '          <div class="poster-slider-dots" data-slider-dots>\n'
        + "\n".join(dots) + "\n"
        "          </div>\n"
        "        </div>"
    )


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
        ("TITLE_EN_META", f" ({p['title_en']})" if p["title_en"] else ""),
        ("ARTIST", p["artist"]),
        ("SNS_BLOCK", sns_block(p)),
        ("DESC", p["desc"]),
        ("IMAGE", p["image"]),
        ("DETAIL_IMAGE_BLOCK", detail_image_block(p)),
        ("PREV_HREF", f"{prev_p['id']}.html"),
        ("PREV_TITLE", prev_p["title_ko"]),
        ("NEXT_HREF", f"{next_p['id']}.html"),
        ("NEXT_TITLE", next_p["title_ko"]),
        ("COUNT", str(n)),
    ]:
        html = html.replace("{{" + key + "}}", val)

    out_path = os.path.join(ROOT, "poster", f"{p['id']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"generated poster/{p['id']}.html")

# ---- gallery.html 생성 ----
cards = []
for p in posters:
    cards.append(f'''      <div class="poster-cell">
        <div class="poster-reveal">
          <a class="poster-card" href="poster/{p['id']}.html">
            <div class="thumb">
              <img src="assets/images/{p['image']}" alt="{p['title_ko']}"
                   onerror="this.remove()">
            </div>
            <div class="meta">
              <div class="num">Platform {p['id']}</div>
              <h3>{p['title_ko']}</h3>
              <div class="artist">{p['artist']}</div>
            </div>
          </a>
        </div>
      </div>''')

gallery_html = gallery_tpl.replace("{{CARDS}}", "\n".join(cards)).replace("{{COUNT}}", str(n))
with open(os.path.join(ROOT, "gallery.html"), "w", encoding="utf-8") as f:
    f.write(gallery_html)
print("generated gallery.html")
