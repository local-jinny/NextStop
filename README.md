# 포스터 아카이브 — 환승역: NEXT STOP

홍익대학교 디자인컨버전스학부 소모임 야와야츠 70주년 여름 방학 전시 `<환승 : NEXT STOP>`을
온라인으로 아카이빙하는 사이트. 랜딩 → 갤러리(아카이브) → 포스터별 상세 페이지 구성.

배포: https://local-jinny.github.io/NextStop/

## 구조

```
index.html                랜딩 페이지 (정적 파일, build.py가 건드리지 않음)
info.html                  크루 소개 페이지 (정적 파일, build.py가 건드리지 않음)
gallery.html               메인 아카이브 — 카드 그리드 (build.py가 생성)
poster/01.html ~ 14.html   포스터별 상세 페이지 (build.py가 생성)

assets/css/style.css      공통 디자인 시스템 (전 페이지 공유)
assets/js/
  random-poster.js         "랜덤 환승" 버튼 — 포스터 상세페이지 중 무작위 이동
  flap.js                  상세페이지 "Platform NN" 배지의 전광판(split-flap) 숫자 애니메이션
  poster-slider.js         상세컷이 여러 장인 포스터(04/06/08)의 이미지 슬라이더
assets/images/
  01.jpg ~ 14.jpg           포스터별 메인 이미지
  04-2.jpg ...              상세컷(포스터별로 개수 다름, data/posters.json의 extra_images 참고)
  08-video.mp4              08번 슬라이드 1번 자리에 들어가는 영상(이미지 대신)
  og-image.jpg              링크 공유 시 미리보기 썸네일(Open Graph 이미지, 1200x630) — 전 페이지 공용
  poster/                   원본 이미지 백업 (고용량, git에는 안 올라감 — .gitignore 참고)

data/posters.json          포스터별 콘텐츠 데이터 (제목, 작가, SNS, 설명, 이미지 파일명 등)
template/                  gallery.html, poster.html의 원본 템플릿 (build.py가 이걸로 최종 html 생성)
scripts/
  build.py                  data + template → gallery.html, poster/*.html 생성 (반복 사용)
  apply_captions.py         스크린샷에서 옮겨적은 실제 캡션을 posters.json에 반영한 1회성 스크립트
  process_poster_images.py  메인 포스터 원본 리사이즈/변환 1회성 스크립트
  process_detail_images.py  상세컷 원본 리사이즈/변환 1회성 스크립트
```

## 콘텐츠 수정 방법 (가장 중요)

1. `data/posters.json`에서 해당 포스터 항목의 `title_ko`, `title_en`, `artist`, `sns`, `desc`를 수정
2. 이미지를 바꾸는 경우 `assets/images/`에 같은 파일명(`01.jpg` 등)으로 덮어쓰기
3. 재생성:
   ```bash
   python3 scripts/build.py
   ```
   → `gallery.html`과 `poster/*.html` 전체가 새 내용으로 다시 만들어짐
   (`index.html`, `info.html`은 정적 파일이라 직접 수정)

### `posters.json` 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| `id` | ✅ | 2자리 번호 문자열 (`"01"` ~ `"14"`) |
| `title_ko` / `title_en` | ✅ | 국문/영문 제목. 하나만 있으면 `title_ko`에 넣고 `title_en`은 빈 문자열 |
| `artist` | ✅ | 작가명 |
| `desc` | ✅ | 작품 설명 |
| `image` | ✅ | 메인 이미지 파일명 (`assets/images/`, 갤러리 카드 썸네일에도 사용) |
| `sns` | 선택 | Instagram 등 URL 1개. 없으면 빈 문자열 `""` → 상세페이지에서 SNS 줄 자체가 숨겨짐 |
| `sns_list` | 선택 | SNS 계정이 여러 개일 때 `[{"url":..., "label":"@handle"}, ...]` 형태로, 각각 독립된 링크로 렌더링(`sns`보다 우선) |
| `extra_images` | 선택 | 상세컷 파일명 배열. 있으면 메인 이미지+상세컷을 스와이프 슬라이더로 표시 |
| `video` | 선택 | 있으면 슬라이더 1번 슬롯을 이미지 대신 `<video autoplay muted loop>`로 표시 (08번 사례) |

## 이미지 규격

- **메인 이미지**(슬라이더 1번 슬롯 포함): 원본 비율 그대로 표시(크롭 없음) — 세로로 긴 포스터가 자연스럽게 보임
- **상세컷**(`extra_images`, 2번 슬롯부터): 인스타그램 피드처럼 4:5로 고정 크롭
- 공통 권장: JPG, 긴 변 기준 1200~1600px, 장당 300~600KB대
  (원본이 이보다 크면 `process_poster_images.py` / `process_detail_images.py` 참고해서 같은 방식으로 리사이즈)

## 로컬 미리보기

```bash
python3 -m http.server 8000
# http://localhost:8000 접속
```

## GitHub 업데이트 워크플로

```bash
cd ~/Desktop/NextStop
python3 scripts/build.py        # 콘텐츠 수정 후 재생성(필요시)
git add .
git commit -m "변경 내용 설명"
git push
```

- push 시 GitHub 아이디 + Personal Access Token 필요(비밀번호 아님). 토큰 만료 시 재발급
  (Settings → Developer settings → Fine-grained tokens, Contents: Read and write 권한 필수)
- push 후 1~2분 내 배포 주소에 자동 반영

## 디자인 시스템 메모

- 배경: 솔리드 네이비(`#333474`) + 랜덤 별 패턴, 포인트 컬러 민트(`#69d1cb`)/크림(`#f9ddaf`)
- 폰트: 본문은 Noto Sans KR. 제목류(작품 제목, `Platform NN` 배지, PREV/NEXT 제목, 랜딩·인포 강조 문구)는
  `--font-title`(영문 Righteous + 한글 Do Hyeon 조합, 둘 다 구글폰트 단일 굵기라 `font-weight`는 항상 400으로 사용)
- 갤러리 카드: 4열(모바일 2열) 벽돌형 배치 + 스크롤 리빌 애니메이션(백스크롤 시 역방향 재생), hover는 별도 wrapper로 분리해 리빌 애니메이션과 타이밍이 서로 안 얽히게 되어 있음(`assets/css/style.css`의 `.poster-cell` / `.poster-reveal` / `.poster-card` 3중 구조 참고)
