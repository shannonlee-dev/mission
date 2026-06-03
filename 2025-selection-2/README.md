# 2025 Selection 2

2025 선발 2차 과제 산출물입니다. Mars 미션 기반 Python 실습, 간단한 웹 페이지, 오디오 처리, CCTV 데이터 처리 과제를 포함합니다.

## Structure

```text
2025-selection-2/
├── assets/
├── devops/
├── python/
│   ├── problem-1/
│   ├── problem-2/
│   ├── problem-3/
│   ├── problem-4/
│   ├── problem-5/
│   ├── problem-6/
│   └── problem-7/
└── tools/
```

## Problem Index

| Path | Summary |
| --- | --- |
| `python/problem-1/` | 미션 컴퓨터 로그 분석 및 JSON 변환 |
| `python/problem-2/` | Mars 기지 인벤토리, 돔 설계, CSV 처리 |
| `python/problem-3/` | Mars Mission Computer 클래스 실습 |
| `python/problem-4/` | 문 해킹 시나리오 및 입출력 처리 |
| `python/problem-5/` | 공학용 계산기 구현 |
| `python/problem-6/` | 음성/오디오 처리 실습과 녹음 자료 |
| `python/problem-7/` | CCTV 데이터 처리 실습 |
| `devops/` | Flask 템플릿 기반 웹 실습 |
| `assets/` | README 및 웹 과제에서 참조하는 이미지 |

## Run

개별 문제 폴더에서 필요한 Python 파일을 실행합니다.

```bash
cd 2025-selection-2/python/problem-1
python3 main.py
```

웹 실습은 `devops/`에서 실행합니다.

```bash
cd 2025-selection-2/devops
python3 app.py
```

## Notes

- 문제 디렉토리는 `problem-N` 형식으로 통일했습니다.
- 외부 라이브러리 또는 큰 소스 묶음은 문제 폴더 안에 유지하되, 산출물과 도구의 역할이 드러나도록 상위 구조를 분리했습니다.
