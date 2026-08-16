#!/usr/bin/env python3
"""~/Desktop/poster/ 원본을 assets/images/poster/에 그대로 복사해둔 파일들을 찾아
작가명으로 매칭해 assets/images/01.jpg ~ 14.jpg로 리사이즈/변환한다.
(사이트가 실제로 읽는 경로는 assets/images/{{IMAGE}} 이지 assets/images/poster/ 하위가 아니므로 최종본은 부모 폴더에 둔다.)

원본(assets/images/poster/*)은 그대로 보존하고 건드리지 않는다.

리사이즈 규칙(README의 "이미지 아카이빙 권장 규격" 기준):
  - 긴 변 기준 최대 1600px로 축소(원본이 더 작으면 그대로 둠)
  - JPG로 저장, 장당 300~600KB대를 목표로 품질을 자동 조정
  - 알파 채널(PNG 투명 영역)은 흰 배경으로 깔고 병합 후 JPG 저장

    python3 scripts/process_poster_images.py
"""
import glob
import os
import unicodedata
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "assets", "images", "poster")
DST_DIR = os.path.join(ROOT, "assets", "images")

MAX_EDGE = 1600
TARGET_MAX_BYTES = 600 * 1024
TARGET_MIN_BYTES = 300 * 1024

# 포스터 번호: 원본 파일명에 포함된 작가명 키워드
ARTIST_BY_ID = {
    "01": "정지민",
    "02": "안하정",
    "03": "이유진",
    "04": "문다희",
    "05": "임하진",
    "06": "신원영",
    "07": "최슬아",
    "08": "이예원",
    "09": "이연우",
    "10": "문서영",
    "11": "정성훈",
    "12": "하예은",
    "13": "장세원",
    "14": "윤여진",
}


def find_source(artist_kw):
    kw_nfc = unicodedata.normalize("NFC", artist_kw)
    candidates = [
        f for f in glob.glob(os.path.join(SRC_DIR, "*"))
        if kw_nfc in unicodedata.normalize("NFC", os.path.basename(f))
        and not f.lower().endswith(".ds_store")
    ]
    if not candidates:
        return None
    if len(candidates) > 1:
        raise SystemExit(f"'{artist_kw}' 관련 파일이 여러 개 발견됨: {candidates}")
    return candidates[0]


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
    for poster_id, artist_kw in ARTIST_BY_ID.items():
        src = find_source(artist_kw)
        if src is None:
            print(f"[SKIP] {poster_id}: '{artist_kw}' 소스 파일을 찾지 못함")
            continue

        im = Image.open(src)
        im = resize_and_flatten(im)

        out_path = os.path.join(DST_DIR, f"{poster_id}.jpg")
        quality, size = save_jpeg_within_budget(im, out_path)

        note = ""
        if size < TARGET_MIN_BYTES:
            note = " (권장 하한 300KB 미만이지만 원본 화질 유지 위해 그대로 둠)"
        print(f"{poster_id}.jpg <- {os.path.basename(src)} | {im.size[0]}x{im.size[1]} | q{quality} | {size/1024:.0f}KB{note}")


if __name__ == "__main__":
    main()
