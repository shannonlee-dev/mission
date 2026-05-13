# 99_HUMAN_REPORT

이 문서는 `11_REQUIREMENTS_MATRIX.md`에 정리된 요구사항을 사람이 빠르게 검토할 수 있도록 다시 정리한 문서다.
프로젝트 전체 진행도는 `11_REQUIREMENTS_MATRIX.md`에서 계산한 결과값만 미러링한다.
이 문서는 DONE 작업 증거 로그를 생성하지 않고, 실제 증거 로그 경로를 참조해 표시한다.
DONE 항목 중 `BLOCKED 경험`이 `0`인 항목은 `runtime/done_logs/<REQ-ID>.log`를 참조한다.
DONE 항목 중 `BLOCKED 경험`이 `1`인 항목은 `runtime/blocked.log`를 참조한다.

## 프로젝트 전체 진행도

- 현재 진행도 : 100%

## 표 1. 요구사항 상태 요약

| 순서 | ID | 분류 | 요구사항 | 증거 로그 | 상태 |
|---:|---|---|---|---|---|
| 1 | ENV-001 | 환경 | 제공된 `agent-app-leak` 바이너리를 리눅스에서 root가 아닌 일반 사용자로 실행한다. | `runtime/done_logs/ENV-001.log` | DONE |
| 2 | ENV-002 | 환경 | 필수 환경변수, 디렉터리, 로그 경로, 키 파일 조건을 충족한다. | `runtime/done_logs/ENV-002.log` | DONE |
| 3 | ENV-003 | 환경 | `0.0.0.0:15034` 바인딩 가능 환경에서 표준 리눅스 도구를 사용한다. | `runtime/done_logs/ENV-003.log` | DONE |
| 4 | SEC-001 | 보안 | 제공 바이너리에 대해 디컴파일 및 리버스 엔지니어링을 시도하지 않는다. | `runtime/done_logs/SEC-001.log` | DONE |
| 5 | FUNC-001 | 기능 | OOM 케이스에서 `monitor.sh`로 메모리 사용량 증가 패턴을 관측한다. | `runtime/done_logs/FUNC-001.log` | DONE |
| 6 | FUNC-002 | 기능 | OOM 케이스에서 MemoryGuard 강제 종료 핵심 로그를 식별한다. | `runtime/blocked.log` | DONE |
| 7 | FUNC-003 | 기능 | `MEMORY_LIMIT` 변경 전후 최소 2회 실행 비교를 OOM 리포트에 기록한다. | `runtime/blocked.log` | DONE |
| 8 | FUNC-004 | 기능 | CPU 케이스에서 특정 프로세스의 CPU 상승 구간을 식별한다. | `runtime/done_logs/FUNC-004.log` | DONE |
| 9 | FUNC-005 | 기능 | CPU 케이스에서 `CPU Threshold Violated` 보호 종료 로그를 입증한다. | `runtime/blocked.log` | DONE |
| 10 | FUNC-006 | 기능 | `CPU_MAX_OCCUPY` 변경 전후 비교를 CPU 리포트에 기록한다. | `runtime/blocked.log` | DONE |
| 11 | FUNC-007 | 기능 | Deadlock 케이스에서 PID 존재와 CPU/메모리/로그 정체를 식별한다. | `runtime/blocked.log` | DONE |
| 12 | FUNC-008 | 기능 | Deadlock 케이스에서 마지막 `WAITING`/`BLOCKED` 로그로 자원 대기 상태를 증명한다. | `runtime/blocked.log` | DONE |
| 13 | FUNC-009 | 기능 | `MULTI_THREAD_ENABLE` 변경 전후 데드락 재현/회피 비교를 기록한다. | `runtime/blocked.log` | DONE |
| 14 | VAL-001 | 검증 | OOM 리포트에 필수 증거 최소 요건을 포함한다. | `runtime/blocked.log` | DONE |
| 15 | VAL-002 | 검증 | CPU 리포트에 필수 증거 최소 요건을 포함한다. | `runtime/blocked.log` | DONE |
| 16 | VAL-003 | 검증 | Deadlock 리포트에 필수 증거 최소 요건을 포함한다. | `runtime/blocked.log` | DONE |
| 17 | DOC-001 | 문서화 | 세 장애 리포트가 GitHub Issue 제목과 4개 필수 섹션 구조를 따른다. | `runtime/done_logs/DOC-001.log` | DONE |
| 18 | SUB-001 | 제출 | 리포트 3건을 PDF 또는 GitHub Repository 링크 형태로 제출할 수 있게 정리한다. | `runtime/done_logs/SUB-001.log` | DONE |
| 19 | BONUS-001 | 보너스 | 로그 패턴으로 스케줄링 알고리즘을 추론하고 장단점 및 적합 아키텍처를 분석한다. | `runtime/blocked.log` | DONE |
| 20 | CHECK-001 | 표준 검증 | 전체 검증 진입점 `scripts/check.sh`를 생성하고 실행 결과를 기록한다. | `runtime/done_logs/CHECK-001.log` | DONE |
| 21 | CHECK-002 | 표준 검증 | 빠른 점검 진입점 `scripts/smoke.sh`를 생성하고 실행 결과를 기록한다. | `runtime/done_logs/CHECK-002.log` | DONE |

## 표 2. 요구사항별 검증 방법

| ID | 확인 명령 | 성공 기준 |
|---|---|---|
| ENV-001 | `grep -n "Agent READY\\|Running as service user" runtime/work.log` | 일반 사용자 실행과 앱 부트 성공이 확인되면 성공 |
| ENV-002 | `grep -n "All required Envs correct\\|Verified 'secret.key'" runtime/work.log` | 필수 환경변수와 키 파일 확인 로그가 있으면 성공 |
| ENV-003 | `grep -n "Port 15034 is available\\|Agent listening at port 15034" runtime/work.log` | 포트 바인딩과 도구 기반 관측 로그가 있으면 성공 |
| SEC-001 | `grep -Ei "decompile|reverse|objdump|gdb|radare|ghidra" runtime/work.log` | 금지 행위 명령이 없으면 성공 |
| FUNC-001 | `grep -n "RSS_MB" runtime/evidence/oom/memory-128/monitor.log` | 대상 프로세스 RSS 증가 수치가 있으면 성공 |
| FUNC-002 | `grep -R "Memory limit exceeded\\|Self-terminating\\|MemoryGuard" runtime/evidence/oom/memory-50 runtime/evidence/oom/memory-128` | MemoryGuard 종료 로그가 확인되면 성공 |
| FUNC-003 | `grep -n "MEMORY_LIMIT=50\\|MEMORY_LIMIT=128" runtime/work.log` | 50/128 비교 실행과 임계치 차이가 확인되면 성공 |
| FUNC-004 | `grep -n "CpuWorker.*Current Load\\|CPU Threshold" runtime/evidence/cpu/cpu-max-100/app.log` | 대상 CPU 상승 및 임계치 위반 로그가 있으면 성공 |
| FUNC-005 | `grep -R "CPU Threshold Violated" runtime/evidence/cpu/cpu-max-100` | CPU 보호 종료 로그가 확인되면 성공 |
| FUNC-006 | `grep -R "Maximum CPU Limit: 10%\\|Maximum CPU Limit: 100%\\|CPU Threshold Violated" runtime/evidence/cpu/cpu-max-10 runtime/evidence/cpu/cpu-max-100` | 10/100 비교 실행과 cooldown/종료 차이가 확인되면 성공 |
| FUNC-007 | `grep -h "^--- sample .*stagnant_count" runtime/evidence/deadlock/multi-true/thread_samples.log` | 로그 크기 정체와 PID 존재가 확인되면 성공 |
| FUNC-008 | `grep -H "WAITING\\|BLOCKED" runtime/evidence/deadlock/multi-true/app.log` | WAITING/BLOCKED 로그가 확인되면 성공 |
| FUNC-009 | `grep -n "MULTI_THREAD_ENABLE=true\\|MULTI_THREAD_ENABLE=false" runtime/work.log` | true/false 비교 실행과 재현/회피 차이가 확인되면 성공 |
| VAL-001 | `grep -n "MemoryGuard" submission/reports/oom.md` | OOM 리포트에 필수 증거 3종이 포함되면 성공 |
| VAL-002 | `grep -n "CPU Threshold" submission/reports/cpu.md` | CPU 리포트에 필수 증거 3종이 포함되면 성공 |
| VAL-003 | `grep -n "WAITING.*BLOCKED" submission/reports/deadlock.md` | Deadlock 리포트에 필수 증거가 포함되면 성공 |
| DOC-001 | `scripts/check.sh` | 세 장애 리포트의 4개 섹션 검증이 성공하면 성공 |
| SUB-001 | `find submission -maxdepth 3 -type f -print` | 제출 대상 리포트와 README가 있으면 성공 |
| BONUS-001 | `grep -n "Round-Robin\\|FCFS\\|Priority" submission/reports/scheduling.md` | 워커 로그와 알고리즘 결론이 확인되면 성공 |
| CHECK-001 | `bash -n scripts/check.sh && scripts/check.sh` | 문법 검사와 전체 검증이 성공하면 성공 |
| CHECK-002 | `bash -n scripts/smoke.sh && scripts/smoke.sh` | 문법 검사와 빠른 점검이 성공하면 성공 |
