# mission1_2 제출물

이 제출물에는 제공된 `agent-app-leak` 바이너리로부터 생성한 GitHub Issue 스타일 사고 보고서가 포함되어 있습니다.

## 파일

- `agent-app-leak/agent-app-leak`: `agent-app-leak.zip`에서 추출한 제공 실행 파일
- `a.md`: 로그 트리거 맵 (agent-troubleshooting 기반)
- `env-default.sh`: 기본 환경 변수
- `reports/oom.md`: OOM 크래시 분석
- `reports/cpu.md`: CPU 지연 / CPU 가드 분석
- `reports/deadlock.md`: 교착상태 진단
- `reports/scheduling.md`: 보너스 스케줄링 추론
- `logs/`: agent-troubleshooting에서 복사한 원시 런타임 로그

## 증거 범위

런타임 증거는 제공된 바이너리 실행만으로 수집했습니다. 디컴파일이나 리버스 엔지니어링은 수행하지 않았습니다.

주요 증거 경로:

- OOM: `runtime/evidence/oom/memory-50/`, `runtime/evidence/oom/memory-128/`
- CPU: `runtime/evidence/cpu/cpu-max-10/`, `runtime/evidence/cpu/cpu-max-100/`
- 교착상태: `runtime/evidence/deadlock/multi-true/`, `runtime/evidence/deadlock/multi-false/`
- 스케줄링: `runtime/evidence/scheduling/round-robin/`
- 추가 원시 로그: `submission/logs/`

