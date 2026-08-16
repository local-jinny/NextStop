#!/usr/bin/env python3
"""~/Downloads/의 상세컷(개인부스) 폴더들을 읽어 파일명 속 번호 순서대로
assets/images/{poster_id}-2.jpg ... 로 리사이즈/변환해 저장한다.
(각 SOURCES 항목의 장수는 data/posters.json의 extra_images 개수와 정확히 일치해야 함)

원본은 건드리지 않고 assets/images/에 새 JPG로만 저장한다.
리사이즈 규칙은 메인 포스터 처리 때와 동일: 긴 변 최대 1600px, JPG, 300~600KB대 목표.

    python3 scripts/process_detail_images.py
"""
import glob
import os
import re
import unicodedata
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST_DIR = os.path.join(ROOT, "assets", "images")

MAX_EDGE = 1600
TARGET_MAX_BYTES = 600 * 1024

SOURCES = [
    {
        "poster_id": "04",
        "dir": "/Users/yeojin/Downloads/개인부스_인스타_문다희_Dream_to_Dream",
    },
    {
        "poster_id": "06",
        "dir": "/Users/yeojin/Downloads/개인부스_인스타2_신원영_실패로 만들어진 세계",
    },
    {
        "poster_id": "08",
        "dir": "/Users/yeojin/Downloads/개인부스_인스타_이예원_Abberation",
        # 08은 슬라이드 1번이 영상(assets/images/08-video.mp4, 수동으로 복사해둔 원본)이라
        # 이 폴더의 정지 이미지(jpg/png)만 처리 대상으로 한정한다.
        "only_ext": (".jpg", ".jpeg", ".png"),
    },
]


def numeric_key(path):
    """파일명 어디든 있는 첫 숫자 기준 정렬. 번호가 아예 없으면(예: 원본 파일) 1번으로 취급.
    ('...Abberation6jpg.jpg'처럼 확장자 바로 앞이 아닌 오타 파일명도 대응)"""
    name = unicodedata.normalize("NFC", os.path.basename(path))
    base = os.path.splitext(name)[0]
    m = re.search(r"\d+", base)
    return int(m.group()) if m else 1


def resize_and_flatten(im):
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg

    w, h = im.size
    longest = max(w, h)
    if longest > MAX_EDGE:
        scale = MAX_EDGE / longest
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    return im


def save_jpeg_within_budget(im, out_path):
    for quality in (90, 85, 80, 75, 70, 65, 60):
        im.save(out_path, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(out_path)
        if size <= TARGET_MAX_BYTES:
            return quality, size
    return quality, os.path.getsize(out_path)


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    for src in SOURCES:
        allowed_ext = src.get("only_ext")
        files = [
            f for f in glob.glob(os.path.join(src["dir"], "*"))
            if not f.lower().endswith(".ds_store")
            and (allowed_ext is None or f.lower().endswith(allowed_ext))
        ]
        files.sort(key=numeric_key)

        for n, path in enumerate(files, start=2):
            im = Image.open(path)
            im = resize_and_flatten(im)
            out_name = f"{src['poster_id']}-{n}.jpg"
            out_path = os.path.join(DST_DIR, out_name)
            quality, size = save_jpeg_within_budget(im, out_path)
            print(f"{out_name} <- {os.path.basename(path)} | {im.size[0]}x{im.size[1]} | q{quality} | {size/1024:.0f}KB")


if __name__ == "__main__":
    main()
