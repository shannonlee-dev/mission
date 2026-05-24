# 2025 Selection Team

2025 팀 선발 과제 산출물입니다. 지도 데이터를 바탕으로 카페 위치와 이동 경로를 처리하고, 제출용 구현과 초안 작업물을 분리해 관리합니다.

## Structure

```text
2025-selection-team/
├── draft/
└── submission/
```

## Contents

| Path | Summary |
| --- | --- |
| `submission/` | 최종 제출 산출물, 지도 처리 스크립트, A* 경로 탐색 구현 |
| `draft/` | 개발 중 작성한 초안 코드, 테스트 코드, 검증 메모 |

## Run

최종 제출물 기준 실행은 `submission/`에서 진행합니다.

```bash
cd 2025-selection-team/submission
python3 map_direct_save_astar.py
```

초안 검증은 `draft/`에서 별도로 실행합니다.

```bash
cd 2025-selection-team/draft
python3 run_tests.py
```

## Notes

- 기존 임시 작업 폴더는 `draft/`로 정리했습니다.
- 최종 평가 대상은 `submission/`을 기준으로 확인합니다.
