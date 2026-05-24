# 2025 Selection Team Submission

팀 선발 과제의 최종 제출 산출물입니다. 지역 지도 CSV를 읽어 구조물과 카페 위치를 분석하고, 집에서 카페까지의 이동 경로를 계산합니다.

## Structure

```text
submission/
├── data/
├── caffee_map.py
├── map_draw.py
├── map_direct_save.py
├── map_direct_save_astar.py
├── requirements.txt
└── setup_environment.sh
```

## Contents

| Path | Summary |
| --- | --- |
| `data/area_map.csv` | 지도 격자 데이터 |
| `data/area_struct.csv` | 구조물 위치와 유형 데이터 |
| `data/area_category.csv` | 구조물 유형 매핑 데이터 |
| `caffee_map.py` | 지도와 구조물 데이터 분석 |
| `map_draw.py` | 지도 시각화 |
| `map_direct_save.py` | 기본 경로 계산 및 저장 |
| `map_direct_save_astar.py` | A* 기반 경로 탐색 구현 |

## Setup

```bash
cd 2025-selection-team/submission
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python3 caffee_map.py
python3 map_draw.py
python3 map_direct_save_astar.py
```

## Notes

- 이 폴더는 최종 제출 기준 산출물입니다.
- 개발 중 검증과 실험 코드는 상위 `draft/` 폴더에 분리했습니다.
