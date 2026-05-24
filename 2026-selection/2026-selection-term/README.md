# 2026 Selection Term

2026 선발 과정 발표 자료와 PDF 변환 도구를 관리하는 디렉토리입니다. HTML 기반 발표 자료를 작성하고, Node.js 스크립트로 슬라이드 PDF 변환 및 병합을 수행합니다.

## Structure

```text
2026-selection-term/
├── index.html
├── ppt_plan.md
├── convert-slides-to-pdf.js
├── merge-pdfs.js
├── package.json
└── package-lock.json
```

## Contents

| Path | Summary |
| --- | --- |
| `index.html` | 발표용 HTML 슬라이드 |
| `ppt_plan.md` | 발표 구성안과 제작 메모 |
| `convert-slides-to-pdf.js` | HTML 슬라이드 PDF 변환 스크립트 |
| `merge-pdfs.js` | 생성된 PDF 병합 스크립트 |
| `package.json` | Node.js 실행 의존성과 명령 정의 |

## Run

```bash
cd 2026-selection-term
npm install
node convert-slides-to-pdf.js
node merge-pdfs.js
```

현재 `package.json`은 의존성만 정의하고 있으며, 실행은 Node.js 스크립트를 직접 호출하는 방식입니다.

## Notes

- 발표 원본은 `index.html`을 기준으로 관리합니다.
- PDF 산출물은 필요할 때 재생성하는 파일로 취급합니다.
