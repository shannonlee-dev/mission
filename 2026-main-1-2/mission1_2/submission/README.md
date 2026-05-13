# mission1_2 Submission

This submission contains GitHub Issue style incident reports produced from the provided `agent-app-leak` binary.

## Files

- `agent-app-leak/agent-app-leak`: provided executable extracted from `agent-app-leak.zip`
- `reports/oom.md`: OOM Crash analysis
- `reports/cpu.md`: CPU Latency / CPU guard analysis
- `reports/deadlock.md`: Deadlock diagnosis
- `reports/scheduling.md`: bonus scheduling inference

## Evidence Scope

Runtime evidence was collected from executing the provided binary only. No decompilation or reverse engineering was performed.

Primary evidence paths:

- OOM: `runtime/evidence/oom/memory-50/`, `runtime/evidence/oom/memory-128/`
- CPU: `runtime/evidence/cpu/cpu-max-10/`, `runtime/evidence/cpu/cpu-max-100/`
- Deadlock: `runtime/evidence/deadlock/multi-true/`, `runtime/evidence/deadlock/multi-false/`
- Scheduling: `runtime/evidence/scheduling/round-robin/`

