# mission1_2 제출물

본 제출물은 제공된 `agent-app-leak` 바이너리에서 생성된 GitHub Issue 스타일의 사고 보고서를 포함하고 있습니다.

## 파일 목록

* `agent-app-leak/agent-app-leak`: `agent-app-leak.zip`에서 추출하여 제공된 실행 파일
* `a.md`: 로그 트리거 맵 (agent-troubleshooting 제공)
* `env-default.sh`: 기본 환경 변수 설정값
* `reports/oom.md`: OOM(메모리 부족) 충돌 분석
* `reports/cpu.md`: CPU 지연 시간 / CPU 가드 분석
* `reports/deadlock.md`: 데드락(교착 상태) 진단
* `reports/scheduling.md`: 보너스 스케줄링 추론
* `logs/`: agent-troubleshooting에서 복사한 원본 런타임 로그

---

## 증거 범위

런타임 증거는 제공된 바이너리를 실행해서만 수집되었습니다. 디컴파일이나 리버스 엔지니어링은 수행되지 않았습니다.

**주요 증거 경로:**

* **OOM**: `runtime/evidence/oom/memory-50/`, `runtime/evidence/oom/memory-128/`
* **CPU**: `runtime/evidence/cpu/cpu-max-10/`, `runtime/evidence/cpu/cpu-max-100/`
* **데드락**: `runtime/evidence/deadlock/multi-true/`, `runtime/evidence/deadlock/multi-false/`
* **스케줄링**: `runtime/evidence/scheduling/round-robin/`
* **추가 원본 로그**: `submission/logs/`