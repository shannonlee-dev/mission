# 2026 Selection 1

개발 워크스테이션 구축 과제입니다. 터미널, Docker, Git/GitHub, VSCode 연동을 실습하고, Nginx 기반 정적 웹 페이지를 컨테이너로 실행한 결과를 정리했습니다.

## Structure

```text
2026-selection-1/
├── Dockerfile
├── app/
│   └── index.html
└── docs/
    └── screenshots/
```

## Contents

| Path | Summary |
| --- | --- |
| `Dockerfile` | Nginx 기반 정적 웹 서버 이미지 정의 |
| `app/index.html` | 컨테이너에서 제공하는 정적 페이지 |
| `docs/screenshots/` | Docker 실행, bind mount, VSCode/GitHub 연동 검증 이미지 |

## Run

```bash
cd 2026-selection-1
docker build -t codyssey-workstation .
docker run --rm -p 8080:80 codyssey-workstation
```

실시간 파일 반영을 확인하려면 bind mount로 실행합니다.

```bash
docker run --rm -p 8080:80 -v "$(pwd -P)/app:/usr/share/nginx/html" codyssey-workstation
```

## Notes

- 실행 코드, 문서, 증거 자료를 각각 루트, `app/`, `docs/screenshots/`로 분리했습니다.
- OS 자동 생성 파일은 제거해 제출물만 남기도록 정리했습니다.
