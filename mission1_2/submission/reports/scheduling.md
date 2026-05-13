# [Analysis] 스케줄링 추론 - 워커 로그 순서로 라운드로빈 여부 판단

## 1. 로그 관찰 개요

정상 모니터링 경로에서 `Thread-A`, `Thread-B`, `Thread-C`가 등록되었고, 각 스레드는 일부만 실행된 뒤 선점되었다가 다시 재개되었다.

## 2. 증거 자료

원본 증거:

- `logs/cpu-max-10.log`

로그 발췌:

```text
[Thread-A] Task Started. Calculating... (20%)
[Thread-A] Preempted. Progress saved at (40%)
[Thread-B] Task Started. Calculating... (20%)
[Thread-B] Preempted. Progress saved at (40%)
[Thread-C] Task Started. Calculating... (20%)
[Thread-C] Preempted. Progress saved at (40%)
[Thread-A] Resumed. Calculating... (60%)
[Thread-B] Resumed. Calculating... (60%)
[Thread-C] Resumed. Calculating... (60%)
```

## 3. 패턴 분석 및 결론

관찰된 순서는 A -> B -> C -> A -> B -> C 형태로 반복되며, 각 턴 사이에 진행 상태를 저장하고 다음 스레드로 넘어간다. 이는 다음 이유로 라운드로빈과 가장 가깝다:

- FCFS라면 `Thread-A`가 완료된 뒤에 `Thread-B`가 시작되어야 하는데, 로그에서는 선점 후 재개가 반복됨.
- 우선순위 스케줄링이라면 특정 스레드가 반복적으로 다른 스레드를 선점해야 하지만 그런 패턴이 없음.

강점:

- 워커 간 공정성.
- 예측 가능한 턴 순서.
- 특정 작업이 런타임을 독점하지 않는 대화형 서비스에 적합.

약점:

- 컨텍스트 스위칭 오버헤드.
- 긴 CPU 버스트가 유리한 배치 처리에는 비효율적.

적합한 사용처:

- 유사한 요청이 다수인 Web/API 워커, 대화형 서비스.

덜 적합한 사용처:

- 처리량이 최우선인 배치 작업.

검증 결과: PASS. 로그 순서가 라운드로빈 패턴과 일치한다.

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

