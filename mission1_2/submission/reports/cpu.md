# [Bug] CPU 지연 - CPU 부하가 안전 임계치를 넘으면 CpuWorker 가드가 에이전트를 종료함

## 1. Description (현상 설명)

CPU 케이스는 데드락 경로를 피하고 CPU 동작만 분리하기 위해 `MULTI_THREAD_ENABLE=false`로 재현했다. 에이전트는 정상적으로 시작했고 `CpuWorker`가 실행됐다. 두 구성을 비교했다:

- 이전: `CPU_MAX_OCCUPY=100`
- 이후: `CPU_MAX_OCCUPY=10`

`CPU_MAX_OCCUPY=100`에서는 `CpuWorker` 부하가 안전 임계치를 넘어 프로세스가 종료됐다. `CPU_MAX_OCCUPY=10`에서는 작업자가 반복해서 `10.00%`에 도달한 뒤 냉각으로 들어가 위반 임계치를 넘지 않았다.

## 2. Evidence & Logs (증거 자료)

원본 증거:

- `logs/cpu-max-100.log`
- `logs/cpu-max-10.log`

스크린샷 (time 연관):

- 2026-05-13 20:21: `ps` 확인 (PID/리소스 스냅샷)

![ps snapshot](../screenshots/command_ps.png)

- 2026-05-13 20:22: `top` 실행 전 (CPU load 1.7)

![top before](../screenshots/comman_top_before.png)

- 2026-05-13 20:22: `top` 실행 후 (CPU load 2.0)

![top after](../screenshots/command_top_after.png)

프로그램 로그 발췌:

```text
CPU_MAX_OCCUPY=100:
[CpuWorker] Started. Maximum CPU Limit: 100%
[CpuWorker] Current Load: 48.26%
[CpuWorker] CPU Threshold Violated! (50.739999999999995%).

CPU_MAX_OCCUPY=10:
[CpuWorker] Started. Maximum CPU Limit: 10%
[CpuWorker] Peak reached (10.00%). Starting cooldown...
```

## 3. Root Cause Analysis (원인 분석)

CPU 이슈는 에이전트의 자체 `CpuWorker` 가드가 제어한다. 완화된 `CPU_MAX_OCCUPY=100`은 부하가 약 `50%`를 넘긴 뒤 `CPU Threshold Violated` 로그가 발생하도록 허용했다. 이는 무작위 크래시가 아니라 보호 종료 경로다.

`CPU_MAX_OCCUPY=10`에서는 작업자가 `10.00%`를 피크로 간주하고 냉각에 들어간다. 비교 결과 환경 변수가 작업 부하가 위반 범위로 상승하는지 여부를 바꾸는 것을 보여준다.

## 4. Workaround & Verification (조치 및 검증)

우회 방법:

- 이 테스트 환경에서는 `10`과 같은 보수적인 `CPU_MAX_OCCUPY`를 사용한다.
- CPU 동작을 데드락 동작과 분리할 때는 `MULTI_THREAD_ENABLE=false`를 유지한다.

이전 및 이후:

- `CPU_MAX_OCCUPY=100`: 부하가 `50.73%`까지 올라가 `CPU Threshold Violated`가 발생.
- `CPU_MAX_OCCUPY=10`: 부하가 `10.00%`에 도달한 뒤 관측 구간 동안 위반 로그 없이 냉각.

검증 결과: PASS. `CPU_MAX_OCCUPY`에 따라 CPU 가드 동작이 달라졌고, 표준 Linux 도구로 프로세스 PID를 캡처했다.

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

