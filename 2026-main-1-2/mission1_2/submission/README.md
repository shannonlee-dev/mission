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
- `evidence/`: 실험/관측 증거 로그 모음
- `tools/monitor_cpu_sampling.sh`: CPU 스파이크용 촘촘한 샘플링 스크립트
- `tools/cpu_spike_analyzer.py`: ΔCPU/Δt 기반 스파이크 분석 도구

## 증거 범위

런타임 증거는 제공된 바이너리 실행만으로 수집했습니다. 디컴파일이나 리버스 엔지니어링은 수행하지 않았습니다.

주요 증거 경로:

- OOM: `submission/evidence/oom/memory-50/`, `submission/evidence/oom/memory-128/`
- CPU: `submission/evidence/cpu/cpu-max-10/`, `submission/evidence/cpu/cpu-max-100/`
- 교착상태: `submission/evidence/deadlock/multi-true/`, `submission/evidence/deadlock/multi-false/`
- 스케줄링: `submission/evidence/scheduling/round-robin/`
- CPU Spike: `submission/evidence/cpu/spike/`
- 추가 원시 로그: `submission/evidence/`

## CPU Spike 분석 흐름 (짧은 간격 샘플링)

CPU 급상승은 cron 대신 짧은 간격 샘플링으로 관찰한다. 흐름은 아래와 같다:

1) monitor.sh로 0.5초~1초 간격의 CPU 시계열을 수집한다.
2) 수집 로그를 ΔCPU/Δt(1차 차분 수치미분)로 분석한다.
3) CSV, 그래프, Markdown 리포트를 생성한다.

예시 명령:

```bash
cd submission

# 1) CPU 시계열 수집 (30초, 0.5초 간격)
INTERVAL=0.5 DURATION=30 OUT_DIR="./evidence/cpu/spike" \
	./tools/monitor_cpu_sampling.sh

# 2) ΔCPU/Δt 분석 및 산출물 생성
./tools/cpu_spike_analyzer.py \
	--input ./evidence/cpu/spike/monitor_cpu.log \
	--csv ./evidence/cpu/spike/cpu_spike.csv \
	--plot ./evidence/cpu/spike/cpu_spike.png \
	--report ./evidence/cpu/spike/cpu_spike.md \
	--threshold 10
```

