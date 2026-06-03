# codyssey-mission

이 저장소는 더 이상 모든 2026 과제를 한곳에 담는 모노레포가 아닙니다. 2026 미션은 각 과제의 내용과 Git 기록을 살려 별도 저장소로 분리했습니다.
Codyssey 미션 산출물을 과제별 독립 저장소로 분리한 뒤, 원본 작업 흐름과 2025년 산출물을 보존하는 아카이브 저장소입니다.

## Current Layout

| Path | Contents |
| --- | --- |
| `2025-main-1/` | Spaceship Titanic 데이터 분석 |
| `2025-selection-1/` | Python 기초, 계산기, Git 학습 과제 |
| `2025-selection-2/` | Mars Python 미션, 웹 앱, 오디오/CCTV 과제 |
| `2025-selection-team/` | 지도 데이터 처리, 시각화, 경로 탐색 팀 과제 |

```text
.
├── 2025-main-1/
├── 2025-selection-1/
├── 2025-selection-2/
└── 2025-selection-team/
```

## Split Repositories

2026 미션은 과제 폴더를 새 저장소의 루트로 승격해 분리했습니다. 커밋 SHA는 새 tree 구조 때문에 바뀌지만, 각 과제 폴더를 건드린 의미 있는 작업 흐름, 작성자, 날짜, 메시지는 보존하는 방향으로 정리했습니다.

| Repository | Source |
| --- | --- |
| `linux-service-ops-automation` | `2026-main-1-1` |
| `system-failure-analysis-lab` | `2026-main-1-2` |
| `personal-finance-cli` | `2026-main-2-1` |
| `mini-redis-data-structures` | `2026-main-3-1` |
| `version-control-simulator` | `2026-main-3-2` |
| `developer-portfolio-site` | `2026-main-4-1` |
| `study-notes-spa` | `2026-main-4-2` |
| `community-workshop-sql-lab` | `2026-main-5-1` |
| `containerized-dev-workstation` | `2026-selection-1` |
| `persistent-quiz-cli` | `2026-selection-2` |
| `matrix-accelerator-simulator` | `2026-selection-3` |

The link-only mission references were handled separately and are not kept as active project folders in this archive.

## How To Navigate

1. Open one of the remaining top-level `2025-*` directories.
2. Read that directory's `README.md` first.
3. Look for problem-specific code under `problem-N/`, `python/`, `devops/`, `draft/`, or `submission/`.
4. Treat generated files, screenshots, logs, and reports as supporting evidence for the relevant mission.

## Directory Conventions

| Name | Meaning |
| --- | --- |
| `problem-N/` | Problem-specific solution files |
| `submission/` | Final submission material |
| `draft/` | Draft or exploratory implementation |
| `docs/` | Documentation and written notes |
| `screenshots/` | Verification images |
| `tools/` | Helper scripts |
| `assets/` | Images, CSV files, or static material |

## Notes

- The repository is intentionally flatter than the original layout.
- 2026 work should be maintained in its independent repositories after the split.
- This archive keeps the remaining 2025 material readable without the old `2025/` wrapper directory.
- Large generated evidence should stay with the project that explains how it was produced.
