# codyssey_mission

Codyssey 미션과 선발 과제 산출물을 연도와 트랙 기준으로 관리하는 `codyssey_mission` 저장소입니다. 각 최상위 디렉토리는 하나의 과제 저장소처럼 읽히도록 구성하며, 과제별 README를 통해 목적, 구조, 실행 방법, 산출물을 확인할 수 있습니다.

## Repository Map

| Path | Description |
| --- | --- |
| `2025-main-1/` | 2025 메인 1차 과제: Spaceship Titanic 데이터 분석 |
| `2025-selection-1/` | 2025 선발 1차 과제: Python 기초, 계산기, Git 학습 |
| `2025-selection-2/` | 2025 선발 2차 과제: Mars 미션 Python 실습 및 웹/오디오 과제 |
| `2025-selection-team/` | 2025 팀 선발 과제: 지도 데이터 처리 및 경로 탐색 |
| `2026-main-1-1/` | 2026 메인 1-1 과제: 운영 절차 및 제출 산출물 |
| `2026-main-1-2/` | 2026 메인 1-2 과제: 리소스 장애 분석 및 증거 정리 |
| `2026-selection-1/` | 2026 선발 1차 과제: 개발 워크스테이션과 Docker 환경 |
| `2026-selection-2/` | 2026 선발 2차 과제: Python 콘솔 퀴즈 게임 |
| `2026-selection-3/` | 2026 선발 3차 과제: Mini NPU 교육용 시뮬레이터 |
| `2026-selection-term/` | 2026 선발 발표 자료: HTML 슬라이드와 PDF 변환 도구 |
| `docs/` | `codyssey_mission` 운영 문서 |

## Naming Convention

- 최상위 과제 디렉토리: `YYYY-track-round` 형식 사용
- 내부 문제 디렉토리: `problem-N` 형식 사용
- 공용 자료: `assets/`, `docs/`, `tools/`, `submission/`, `runtime/` 등 역할 기반 이름 사용
- 임시 또는 초안 산출물: `draft/` 사용
- README는 최상위 과제 디렉토리마다 1개씩 유지

## Branch Convention

가져온 원본 브랜치는 다음 형식으로 보존합니다.

```text
import/<project-path>/<branch-name>
```

예시는 다음과 같습니다.

```text
import/2025-main-1/main
import/2025-selection-team/submission/main
import/2026-selection-2/feature/play-quiz
```

## Maintenance

- 새 과제를 추가할 때는 최상위에 `YYYY-track-round/` 디렉토리를 만들고 README를 먼저 작성합니다.
- 과제 내부 산출물은 실행 코드, 문서, 증거 자료, 도구를 역할별 디렉토리로 분리합니다.
- OS가 자동 생성한 파일(`.DS_Store`, `__MACOSX` 등)은 커밋하지 않습니다.

## Documents

- [Import Guide](docs/import-guide.md)
