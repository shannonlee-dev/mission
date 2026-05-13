# 98_PROCEDURE_MANUAL

## 1. 작업 기록 폴더 만들기

1. 홈 폴더에 미션 작업 폴더를 만든다.

복붙 명령어:
~~~sh
mkdir -p "$HOME/agent-troubleshooting/reports" "$HOME/agent-troubleshooting/logs" "$HOME/agent-troubleshooting/screenshots"
cd "$HOME/agent-troubleshooting"
pwd
~~~

예상 화면/출력:
~~~text
/home/<현재사용자이름>/agent-troubleshooting
~~~

## 2. 기본 환경 확인하기

1. root 사용자가 아닌지 확인한다.

복붙 명령어:
~~~sh
id -un
test "$(id -u)" -ne 0 && echo "일반 사용자입니다"
~~~

예상 화면/출력:
~~~text
<현재사용자이름>
일반 사용자입니다
~~~

2. 리눅스 명령어가 있는지 확인한다.

복붙 명령어:
~~~sh
command -v ps
command -v top
command -v kill
command -v tee
~~~

예상 화면/출력:
~~~text
/usr/bin/ps
/usr/bin/top
/usr/bin/kill
/usr/bin/tee
~~~

## 3. 필요한 프로그램 설치하기

1. 화면 캡처와 프로세스 확인 도구가 필요하면 설치한다.

복붙 명령어:
~~~sh
sudo apt update
sudo apt install -y htop psmisc gnome-screenshot #GUI 환경이 아니면 gnome-screenshot 불가
~~~

예상 화면/출력:
~~~text
패키지 목록을 읽는 중...
htop, psmisc, gnome-screenshot 설치 또는 이미 설치됨
~~~

## 4. 미션에서 사용할 값 정하기

1. 앱 실행에 사용할 기본 폴더와 환경변수를 준비한다.

복붙 명령어:
~~~sh
mkdir -p "$HOME/agent-app/upload_files" "$HOME/agent-app/api_keys" "$HOME/agent-app/logs"
printf 'agent_api_key_test\n' > "$HOME/agent-app/api_keys/secret.key"
chmod 600 "$HOME/agent-app/api_keys/secret.key"
cat > "$HOME/agent-troubleshooting/env-default.sh" <<'EOF'
export AGENT_HOME="$HOME/agent-app"
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR="$AGENT_HOME/upload_files"
export AGENT_KEY_PATH="$AGENT_HOME/api_keys"
export AGENT_LOG_DIR="$AGENT_HOME/logs"
export MEMORY_LIMIT=256
export CPU_MAX_OCCUPY=10
export MULTI_THREAD_ENABLE=false
EOF
~~~

예상 화면/출력:
~~~text
명령이 끝나고 오류가 없으면 다음 단계로 진행
~~~

2. 제공받은 앱 파일과 관제 스크립트를 작업 폴더에 둔다.

복붙 명령어:
~~~sh
cp <agent-app-leak_파일경로> "$HOME/agent-troubleshooting/agent-app-leak"
cp <monitor.sh_파일경로> "$HOME/agent-troubleshooting/monitor.sh"
chmod u+x "$HOME/agent-troubleshooting/agent-app-leak" "$HOME/agent-troubleshooting/monitor.sh"
ls -l "$HOME/agent-troubleshooting/agent-app-leak" "$HOME/agent-troubleshooting/monitor.sh"
~~~

예상 화면/출력:
~~~text
-rwx... agent-app-leak
-rwx... monitor.sh
~~~

## 5. 단계별 복붙 절차

1. 기본 환경으로 앱을 실행하고 로그를 저장한다.

복붙 명령어:
~~~sh
cd "$HOME/agent-troubleshooting"
. ./env-default.sh
./agent-app-leak 2>&1 | tee "logs/app-default.log"
~~~

예상 화면/출력:
~~~text
앱 시작 로그와 진행 로그가 표시됨
~~~

2. 다른 터미널에서 관제 로그를 저장한다.

복붙 명령어:
~~~sh
cd "$HOME/agent-troubleshooting"
./monitor.sh 2>&1 | tee "logs/monitor-default.log"
~~~

예상 화면/출력:
~~~text
PROCESS:agent-app-leak CPU:<수치>% MEM:<수치>% ...
~~~

3. OOM 분석용으로 메모리 제한을 바꾸어 두 번 비교 실행한다.

복붙 명령어:
~~~sh
cd "$HOME/agent-troubleshooting"
. ./env-default.sh
MEMORY_LIMIT=50 CPU_MAX_OCCUPY=100 MULTI_THREAD_ENABLE=false ./agent-app-leak 2>&1 | tee "logs/oom-memory-50.log"
MEMORY_LIMIT=128 CPU_MAX_OCCUPY=100 MULTI_THREAD_ENABLE=false ./agent-app-leak 2>&1 | tee "logs/oom-memory-128.log"
~~~

예상 화면/출력:
~~~text
각 실행 로그에 MemoryGuard와 Self-terminating 메시지, 생존 시간 차이가 기록됨
~~~

4. CPU 분석용으로 CPU 제한을 바꾸어 비교 실행한다.

복붙 명령어:
~~~sh
cd "$HOME/agent-troubleshooting"
. ./env-default.sh
MEMORY_LIMIT=512 MULTI_THREAD_ENABLE=false CPU_MAX_OCCUPY=10 ./agent-app-leak 2>&1 | tee "logs/cpu-max-10.log"
MEMORY_LIMIT=512 MULTI_THREAD_ENABLE=false CPU_MAX_OCCUPY=100 ./agent-app-leak 2>&1 | tee "logs/cpu-max-100.log"
~~~

예상 화면/출력:
~~~text
10 조건에서는 Peak reached와 cooldown 로그가 보이고, 100 조건에서는 CPU Threshold Violated 로그가 보임
~~~

5. CPU 사용률이 올라가는 순간을 확인한다.

복붙 명령어:
~~~sh
ps -eo pid,comm,pcpu,pmem,args | grep '[a]gent-app-leak'
top -b -n 1 -w 200 | grep 'agent-app-leak'
~~~

예상 화면/출력:
~~~text
agent-app-leak 프로세스의 PID, CPU%, MEM%가 표시됨
~~~

6. Deadlock 분석용으로 멀티스레드 설정을 바꾸어 비교 실행한다.

복붙 명령어:
~~~sh
cd "$HOME/agent-troubleshooting"
. ./env-default.sh
MEMORY_LIMIT=512 CPU_MAX_OCCUPY=10 MULTI_THREAD_ENABLE=true ./agent-app-leak 2>&1 | tee "logs/deadlock-multi-true.log"
MEMORY_LIMIT=512 CPU_MAX_OCCUPY=10 MULTI_THREAD_ENABLE=false ./agent-app-leak 2>&1 | tee "logs/deadlock-multi-false.log"
~~~

예상 화면/출력:
~~~text
true 실행에서는 WAITING/BLOCKED 로그와 멈춤 상태가 보이고, false 실행에서는 회피 결과가 기록됨
~~~

7. 멈춘 프로세스와 스레드 상태를 확인한다.

복붙 명령어:
~~~sh
ps -ef | grep '[a]gent-app-leak'
ps -L -p <PID번호> -o pid,tid,stat,pcpu,pmem,comm
top -H -b -n 1 -p <PID번호>
~~~

예상 화면/출력:
~~~text
PID와 스레드 목록이 보이고 CPU/MEM 변화가 거의 없는지 확인할 수 있음
~~~

## 6. 로그와 출력 기록하기

1. OOM 리포트 초안을 만든다.

복붙 명령어:
~~~sh
cat > "$HOME/agent-troubleshooting/reports/oom.md" <<'EOF'
[Bug] OOM Crash - <한 줄 요약>

## 1. Description (현상 설명)
- 

## 2. Evidence & Logs (증거 자료)
- monitor.sh 관제 로그:
- 프로그램 실행 로그:
- ps/top 출력:

## 3. Root Cause Analysis (원인 분석)
- 

## 4. Workaround & Verification (조치 및 검증)
- MEMORY_LIMIT 변경 전:
- MEMORY_LIMIT 변경 후:
EOF
~~~

예상 화면/출력:
~~~text
reports/oom.md 파일이 만들어짐
~~~

2. CPU 리포트 초안을 만든다.

복붙 명령어:
~~~sh
cat > "$HOME/agent-troubleshooting/reports/cpu.md" <<'EOF'
[Bug] CPU Latency - <한 줄 요약>

## 1. Description (현상 설명)
- 

## 2. Evidence & Logs (증거 자료)
- monitor.sh 관제 로그:
- CPU Threshold 실행 로그:
- ps/top 출력:

## 3. Root Cause Analysis (원인 분석)
- 

## 4. Workaround & Verification (조치 및 검증)
- CPU_MAX_OCCUPY 변경 전:
- CPU_MAX_OCCUPY 변경 후:
EOF
~~~

예상 화면/출력:
~~~text
reports/cpu.md 파일이 만들어짐
~~~

3. Deadlock 리포트 초안을 만든다.

복붙 명령어:
~~~sh
cat > "$HOME/agent-troubleshooting/reports/deadlock.md" <<'EOF'
[Bug] Deadlock - <한 줄 요약>

## 1. Description (현상 설명)
- 

## 2. Evidence & Logs (증거 자료)
- PID 존재 증거:
- CPU/MEM 정체 증거:
- 마지막 WAITING/BLOCKED 로그:

## 3. Root Cause Analysis (원인 분석)
- 

## 4. Workaround & Verification (조치 및 검증)
- MULTI_THREAD_ENABLE=true:
- MULTI_THREAD_ENABLE=false:
EOF
~~~

예상 화면/출력:
~~~text
reports/deadlock.md 파일이 만들어짐
~~~

## 7. 최종 산출물 확인하기

1. 리포트 3개가 있는지 확인한다.

복붙 명령어:
~~~sh
ls -l "$HOME/agent-troubleshooting/reports/oom.md" \
      "$HOME/agent-troubleshooting/reports/cpu.md" \
      "$HOME/agent-troubleshooting/reports/deadlock.md"
~~~

예상 화면/출력:
~~~text
oom.md, cpu.md, deadlock.md 파일 3개가 표시됨
~~~

2. 각 리포트에 4개 섹션이 있는지 확인한다.

복붙 명령어:
~~~sh
grep -R "^## 1\\. Description\\|^## 2\\. Evidence & Logs\\|^## 3\\. Root Cause Analysis\\|^## 4\\. Workaround & Verification" "$HOME/agent-troubleshooting/reports"
~~~

예상 화면/출력:
~~~text
각 리포트마다 Description, Evidence & Logs, Root Cause Analysis, Workaround & Verification 줄이 표시됨
~~~

3. 제출용 PDF가 필요하면 리포트를 하나로 묶는다.

복붙 명령어:
~~~sh
cd "$HOME/agent-troubleshooting"
cat reports/oom.md reports/cpu.md reports/deadlock.md > reports/final-report.md
ls -l reports/final-report.md
~~~

예상 화면/출력:
~~~text
reports/final-report.md 파일이 표시됨
~~~
