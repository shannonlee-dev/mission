# 2025 Selection Team Draft

팀 선발 과제의 초안 및 검증용 작업 공간입니다. 최종 제출 전 작성한 구현, 테스트 코드, 검증 리포트를 보관합니다.

## Structure

```text
draft/
├── data/
├── test/
├── caffee_map.py
├── map_draw.py
├── map_direct_save.py
├── run_tests.py
├── requirements.txt
└── setup_environment.sh
```

## Contents

| Path | Summary |
| --- | --- |
| `data/` | 지도, 구조물, 카테고리 CSV 데이터 |
| `test/` | 단위 및 통합 테스트 코드 |
| `run_tests.py` | 테스트 실행 보조 스크립트 |
| `caffee_map.py` | 데이터 분석 초안 |
| `map_draw.py` | 지도 시각화 초안 |
| `map_direct_save.py` | 경로 저장 로직 초안 |

## Setup

```bash
cd 2025-selection-team/draft
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Verify

```bash
python3 run_tests.py
```

또는 테스트 디렉토리를 직접 실행합니다.

```bash
python3 -m pytest test/
```

## Notes

- 이 폴더는 개발 이력 보존과 검증 목적의 초안 공간입니다.
- 평가 기준 산출물은 `../submission/`을 우선 확인합니다.
