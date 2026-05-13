# [Bug] 데드락 - 동시 작업자가 서로의 리소스를 무기한 대기함

## 1. Description (현상 설명)

데드락 케이스는 제공된 바이너리를 `MULTI_THREAD_ENABLE=true`로 실행해 재현했다. 에이전트는 정상적으로 부팅되고 PID는 유지됐지만, 두 작업자가 각각 하나의 리소스를 점유한 뒤 다른 리소스를 기다리면서 진행이 멈췄다.

비교 실행에서는 `MULTI_THREAD_ENABLE=false`를 사용했고, 정상 모니터링 경로가 선택되어 WAITING/BLOCKED 로그 없이 스케줄러 작업이 완료됐다.

## 2. Evidence & Logs (증거 자료)

원본 증거:

- `logs/deadlock-multi-true.log`
- `logs/deadlock-multi-false.log`

마지막 블로킹 로그:

```text
[Worker-Thread-1] Need resource [Socket_Pool_B] to finish job.
[Worker-Thread-2] Need resource [Shared_Memory_A] to write logs.
[Worker-Thread-1] WAITING for [Socket_Pool_B]... (Status: BLOCKED)
[Worker-Thread-2] WAITING for [Shared_Memory_A]... (Status: BLOCKED)
```

## 3. Root Cause Analysis (원인 분석)

로그는 순환 대기를 보여준다:

- 작업자 1이 `Shared_Memory_A`를 보유하고 `Socket_Pool_B`를 대기.
- 작업자 2가 `Socket_Pool_B`를 보유하고 `Shared_Memory_A`를 대기.

이는 데드락의 핵심 패턴(상호 배제, 점유-대기, 관찰된 흐름에서의 비선점, 순환 대기)을 충족한다. 작업자가 막혀 있었기 때문에 CPU와 메모리는 대부분 유휴 상태였다.

## 4. Workaround & Verification (조치 및 검증)

우회 방법:

- 동시 잠금 경로를 피하려면 `MULTI_THREAD_ENABLE=false`로 설정한다.
- 영구 해결을 위해 공유 리소스를 전역적으로 일관된 순서로 잠그거나 잠금 획득에 타임아웃/백오프를 적용한다.

이전 및 이후:

- `MULTI_THREAD_ENABLE=true`: WAITING/BLOCKED 로그가 발생했고 로그 크기 변화가 멈춤.
- `MULTI_THREAD_ENABLE=false`: 앱이 `Healthy System Monitoring`을 선택했고 WAITING/BLOCKED 로그 없이 스케줄러 작업이 완료됨.

검증 결과: PASS. true/false 비교로 재현 가능한 데드락과 명확한 회피 경로가 확인됐다.

## 부록: 시나리오별 로그 트리거

이 파일은 요청된 로그 문구를 이 저장소에서 관찰된 조건과 매핑합니다.

### OOM (메모리 제한 초과 / 자기 종료)

관찰된 조건:
- MemoryWorker 힙이 MEMORY_LIMIT에 도달하거나 초과할 때까지 증가함.
- MemoryGuard가 "Memory limit exceeded"를 기록하고 즉시 프로세스를 자기 종료함.

증거:
- logs/oom-memory-50.log
	- [MemoryWorker] Current Heap: 50MB
	- [MemoryGuard] Memory limit exceeded (50MB >= 50MB)
	- [MemoryGuard] Self-terminating process ...
- logs/oom-memory-128.log
	- [MemoryWorker] Current Heap: 150MB
	- [MemoryGuard] Memory limit exceeded (150MB >= 128MB)
	- [MemoryGuard] Self-terminating process ...
- logs/app-default.log
	- [MemoryWorker] Current Heap: 275MB
	- [MemoryGuard] Memory limit exceeded (275MB >= 256MB)
	- [MemoryGuard] Self-terminating process ...

### CPU (WATCHDOG / SIGTERM)

검색 결과:
- 이 저장소에서 WATCHDOG 또는 SIGTERM 로그를 찾지 못함.

관찰된 CPU 관련 가장 가까운 동작:
- CpuWorker가 CPU_MAX_OCCUPY에서 최고치를 찍고 종료 없이 진정됨.
	- logs/cpu-max-10.log (최고 10% 후 진정)
	- logs/cpu-max-100.log (최고 40% 후 진정)

WATCHDOG/SIGTERM 경로가 존재하더라도, 해당 로그는 이 작업공간에 없음.

### 교착상태 (WAITING / BLOCKED)

관찰된 조건:
- MULTI_THREAD_ENABLE=true가 동시 작업자를 활성화함.
- 두 작업자 스레드가 서로 다른 리소스를 잠근 뒤 서로를 기다림.
- "Need resource" 메시지 직후 WAITING과 BLOCKED 로그가 나타남.

증거:
- logs/deadlock-multi-true.log
	- [AgentWorker] Waiting for worker threads to complete transactions...
	- [AgentWorker][Worker-Thread-1] WAITING for [Socket_Pool_B]... (Status: BLOCKED)
	- [AgentWorker][Worker-Thread-2] WAITING for [Shared_Memory_A]... (Status: BLOCKED)

