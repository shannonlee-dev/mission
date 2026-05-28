# codyssey-mission

Codyssey 선발/메인 미션 산출물을 한곳에 모아 둔 모노레포입니다.

이 저장소는 과제별 제출 코드, 실행 결과, 분석 문서, 스크린샷, 운영 증거 자료를 연도와 트랙 기준으로 정리합니다. 각 과제 디렉토리는 독립 저장소처럼 읽히도록 구성했고, 세부 실행 방법은 과제별 `README.md`에 둡니다.

## What Is Here

| Path | Contents |
| --- | --- |
| `2025/2025-selection-1/` | Python 기초, 계산기, Git 학습 과제 |
| `2025/2025-selection-2/` | Mars Python 미션, 웹 앱, 오디오/CCTV 과제 |
| `2025/2025-selection-team/` | 지도 데이터 처리, 시각화, 경로 탐색 팀 과제 |
| `2025/2025-main-1/` | Spaceship Titanic 데이터 분석 |
| `2026-selection/2026-selection-1/` | Docker 기반 웹 환경 구성 과제 |
| `2026-selection/2026-selection-2/` | Python 콘솔 퀴즈 게임 |
| `2026-selection/2026-selection-3/` | Mini NPU 시뮬레이터와 CPU/GPU/NPU 시각화 |
| `2026-selection/2026-selection-term/` | HTML 발표 슬라이드와 PDF 변환 도구 |
| `2026-main-1-1/` | 시스템 운영 스크립트, 절차서, 실행 보고서 |
| `2026-main-1-2/` | 리소스 장애 재현, 모니터링 증거, 분석 보고서 |
| `2026-main-2-1/` | 파일 기반 예산 관리 CLI |
| `2026-main-2-2/` | 과제 제출용 저장소 링크 노트 |
| `2026-main-3-1/` | 자료구조 기반 Mini Redis 구현 |
| `2026-main-3-2/` | MiniGit 구현과 diff/LCS 설명 |
| `2026-main-4-1/` | 포트폴리오 웹 페이지 |
| `docs/2026-main-4-1/` | 포트폴리오 페이지 배포용 미러 |

## Repository Layout

```text
.
├── 2025/
│   ├── 2025-selection-1/
│   ├── 2025-selection-2/
│   ├── 2025-selection-team/
│   └── 2025-main-1/
├── 2026-selection/
│   ├── 2026-selection-1/
│   ├── 2026-selection-2/
│   ├── 2026-selection-3/
│   └── 2026-selection-term/
├── 2026-main-*/
└── docs/
```

## How To Navigate

1. 관심 있는 과제 디렉토리로 이동합니다.
2. 해당 디렉토리의 `README.md`를 먼저 읽습니다.
3. 실행 코드는 보통 `main.py`, `app.py`, 패키지 디렉토리, 또는 `submission/` 아래에 있습니다.
4. 증거 자료와 산출물은 `docs/`, `screenshots/`, `reports/`, `runtime/`, `evidence/` 같은 역할 기반 디렉토리에 있습니다.

## Common Directory Names

| Name | Meaning |
| --- | --- |
| `problem-N/` | 문제 번호별 풀이 |
| `submission/` | 최종 제출본 |
| `runtime/` | 실행 중 생성되거나 검증에 사용한 자료 |
| `docs/` | 설명 문서, 보고서, 배포용 문서 |
| `reports/` | 분석/검증 보고서 |
| `screenshots/` | 제출 증빙 이미지 |
| `tools/` | 보조 스크립트 |
| `assets/` | 이미지, CSV, 기타 정적 자료 |
| `draft/` | 초안 또는 작업 중 산출물 |

## Development Notes

- 각 과제는 가능한 한 자기 디렉토리 안에서 독립적으로 실행되도록 둡니다.
- 실행 방법, 의존성, 제출 기준은 과제별 `README.md`에 기록합니다.
- OS 자동 생성 파일과 개인 환경 파일은 커밋하지 않습니다.
- 큰 외부 번들 또는 증거 자료가 필요한 과제는 해당 과제 디렉토리 안에서 출처와 용도를 설명합니다.

## History

기존 `main`의 세부 작업 커밋은 미션/문제 단위로 정리된 히스토리로 재작성했습니다. 과거 히스토리는 다음 ref에 보존되어 있습니다.

```text
backup/main-before-history-cleanup
```

현재 `main`은 최종 파일 상태를 유지하면서 과제 단위로 읽히도록 정리된 커밋 히스토리를 사용합니다.
