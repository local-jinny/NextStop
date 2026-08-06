# Poster Archive

그래픽 포스터 온라인 전시 아카이빙 사이트. 랜딩 페이지 → 메인 아카이브 → 포스터별 상세 페이지 구성.

## 구조

```
index.html               랜딩 페이지 (정적 파일, build.py가 건드리지 않음)
gallery.html              메인 아카이브 — 12장 카드 그리드 (build.py가 생성)
poster/01.html ~ 12.html  포스터별 상세 페이지 (build.py가 생성)
assets/css/style.css     공통 디자인 시스템
assets/images/           포스터 이미지(01.jpg~12.jpg) + Title.svg(랜딩 타이틀)
data/posters.json        포스터별 콘텐츠 (한/영 제목, 작가, SNS, 설명 등)
template/                gallery.html, poster.html의 원본 템플릿
scripts/build.py         data + template → gallery.html, poster/*.html 생성
```

## 콘텐츠 수정 방법

1. `data/posters.json`에서 제목(한/영), 작가, SNS 링크, 설명 등을 수정
2. `assets/images/`에 `01.jpg` ~ `12.jpg` 형식으로 포스터 이미지 추가
3. 아래 명령 실행 → `gallery.html`과 `poster/*.html`이 새로 생성됨 (`index.html`은 정적이라 재생성 안 됨)

```bash
python3 scripts/build.py
```

## 로컬 미리보기

```bash
python3 -m http.server 8000
# http://localhost:8000 접속
```

## 배포 (GitHub Pages)

1. GitHub에 새 저장소 생성 후 이 폴더를 push
2. 저장소 Settings → Pages → Source를 `main` 브랜치 `/ (root)`로 설정
3. `https://<username>.github.io/<repo>/` 로 접속 가능
