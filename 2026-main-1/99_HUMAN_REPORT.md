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
| 1 | ENV-001 | 환경 | Ubuntu 22.04 LTS 또는 동등 Linux 환경에서 수행한다. | `runtime/done_logs/ENV-001.log` | DONE |
| 2 | SEC-001 | 보안 | SSH 접속 포트를 `20022`로 변경한다. | `runtime/blocked.log` | DONE |
| 3 | SEC-002 | 보안 | Root 원격 로그인을 차단한다. | `runtime/blocked.log` | DONE |
| 4 | SEC-003 | 보안 | UFW 또는 firewalld 중 하나를 활성화하고 인바운드는 `20022/tcp`, `15034/tcp`만 허용한다. | `runtime/blocked.log` | DONE |
| 5 | PERM-001 | 권한/계정 | `agent-admin`, `agent-dev`, `agent-test` 계정을 생성한다. | `runtime/blocked.log` | DONE |
| 6 | PERM-002 | 권한/계정 | `agent-common` 그룹은 admin/dev/test, `agent-core` 그룹은 admin/dev를 포함하도록 생성한다. | `runtime/blocked.log` | DONE |
| 7 | PERM-003 | 권한/계정 | `$AGENT_HOME`, `$AGENT_HOME/upload_files`, `$AGENT_HOME/api_keys`, `/var/log/agent-app` 디렉터리 구조를 만든다. | `runtime/blocked.log` | DONE |
| 8 | PERM-004 | 권한/계정 | `upload_files`는 `agent-common` 그룹이 읽고 쓸 수 있게 한다. | `runtime/blocked.log` | DONE |
| 9 | PERM-005 | 권한/계정 | `api_keys` 및 `/var/log/agent-app`는 `agent-core` 그룹만 읽고 쓸 수 있게 한다. | `runtime/blocked.log` | DONE |
| 10 | ENV-002 | 환경 | `AGENT_HOME`, `AGENT_PORT`, `AGENT_UPLOAD_DIR`, `AGENT_KEY_PATH`, `AGENT_LOG_DIR` 환경 변수를 명세 값으로 구성한다. | `runtime/blocked.log` | DONE |
| 11 | DATA-001 | 데이터 | `$AGENT_HOME/api_keys/t_secret.key`에 요구된 키 문자열 1줄을 생성하고 증거에는 마스킹한다. | `runtime/blocked.log` | DONE |
| 12 | APP-001 | 기능 | 앱을 루트가 아닌 일반 계정으로 실행하고 Boot Sequence 5단계 `[OK]` 및 `Agent READY`를 확인한다. | `runtime/blocked.log` | DONE |
| 13 | APP-002 | 기능 | 앱이 `0.0.0.0:15034`로 LISTEN 상태가 되게 한다. | `runtime/blocked.log` | DONE |
| 14 | MON-001 | 기능 | `$AGENT_HOME/bin/monitor.sh`를 Bash로 작성하고 owner `agent-dev`, group `agent-core`, mode `750`으로 설정한다. | `runtime/blocked.log` | DONE |
| 15 | MON-002 | 기능 | `monitor.sh`가 `agent_app.py` 또는 실제 제공 앱 파일명 프로세스 실행 상태를 확인하고 비정상 시 exit `1`로 종료한다. | `runtime/blocked.log` | DONE |
| 16 | MON-003 | 기능 | `monitor.sh`가 TCP `15034` LISTEN 상태를 확인하고 비정상 시 exit `1`로 종료한다. | `runtime/blocked.log` | DONE |
| 17 | MON-004 | 기능 | `monitor.sh`가 방화벽 활성화 상태를 점검하고 비활성 상태면 `[WARNING]`을 출력하되 종료하지 않는다. | `runtime/blocked.log` | DONE |
| 18 | MON-005 | 기능 | `monitor.sh`가 CPU 사용률, 메모리 사용률, 루트 파티션 디스크 사용률을 수집한다. | `runtime/blocked.log` | DONE |
| 19 | MON-006 | 기능 | `monitor.sh`가 CPU `>20%`, MEM `>10%`, DISK_USED `>80%` 조건에서 `[WARNING]`을 출력한다. | `runtime/blocked.log` | DONE |
| 20 | MON-007 | 기능 | `monitor.sh`가 `/var/log/agent-app/monitor.log`에 지정 형식으로 누적 기록한다. | `runtime/blocked.log` | DONE |
| 21 | MON-008 | 기능 | `monitor.log` 용량 관리를 최대 `10MB/10개` 파일 유지로 구현한다. | `runtime/blocked.log` | DONE |
| 22 | CRON-001 | 기능 | `agent-admin` 계정의 crontab으로 `monitor.sh`를 매분 실행 등록한다. | `runtime/blocked.log` | DONE |
| 23 | CRON-002 | 기능 | cron 등록 후 1~2분 내 `monitor.log`에 새 라인이 자동 누적되는 것을 확인한다. | `runtime/blocked.log` | DONE |
| 24 | DOC-001 | 문서화 | 요구사항 수행 내역서에 설정/명령어 기록과 필수 증거 자료 체크리스트를 작성한다. | `runtime/done_logs/DOC-001.log` | DONE |
| 25 | SUB-001 | 제출 산출물 | 요구사항 수행 내역서 문서 1개를 제출 산출물로 준비한다. | `runtime/done_logs/SUB-001.log` | DONE |
| 26 | SUB-002 | 제출 산출물 | 자동화 스크립트 소스코드 `monitor.sh`를 제출 산출물로 준비한다. | `runtime/done_logs/SUB-002.log` | DONE |
| 27 | CHECK-001 | 표준 검증 | 실제 수행 단계에서 전체 검증 진입점 `scripts/check.sh`를 생성하고 실행 결과를 기록한다. | `runtime/work.log`, `runtime/blocked.log` | DONE |
| 28 | CHECK-002 | 표준 검증 | 실제 수행 단계에서 빠른 핵심 점검 진입점 `scripts/smoke.sh`를 생성하고 실행 결과를 기록한다. | `runtime/work.log`, `runtime/blocked.log` | DONE |
| 29 | BONUS-001 | 보너스 | 실제 수행 시 `report.sh`로 `monitor.log`의 CPU/MEM/DISK 평균/최대/최소와 샘플 수를 출력한다. | `runtime/done_logs/BONUS-001.log` | DONE |
| 30 | BONUS-002 | 보너스 | 실제 수행 시 7일 경과 로그 압축, 아카이브 이동, 30일 경과 아카이브 삭제 정책을 구현한다. | `runtime/done_logs/BONUS-002.log` | DONE |

## 표 2. 요구사항별 검증 방법

| ID | 확인 명령 | 성공 기준 |
|---|---|---|
| ENV-001 | `cat /etc/os-release` | Ubuntu 22.04 또는 동등 Linux 환경임을 확인한다. |
| SEC-001 | `sudo sshd -T` 및 `ss -tulnp` | sshd 설정 포트가 `20022`이고 LISTEN 상태가 보인다. |
| SEC-002 | `sudo sshd -T` | `permitrootlogin no`가 보인다. |
| SEC-003 | `sudo ufw status` 또는 `sudo firewall-cmd --list-all` | 방화벽이 활성화되어 있고 `20022/tcp`, `15034/tcp`만 허용된다. |
| PERM-001 | `id agent-admin && id agent-dev && id agent-test` | 세 계정의 UID/GID 정보가 모두 출력된다. |
| PERM-002 | `id agent-admin && id agent-dev && id agent-test` | 그룹 멤버십이 `agent-common`, `agent-core` 정책과 일치한다. |
| PERM-003 | `ls -ld /home/agent-admin/agent-app /home/agent-admin/agent-app/upload_files /home/agent-admin/agent-app/api_keys /var/log/agent-app` | 네 디렉터리가 모두 존재한다. |
| PERM-004 | `ls -ld /home/agent-admin/agent-app/upload_files && getfacl /home/agent-admin/agent-app/upload_files` | 그룹이 `agent-common`이고 그룹 읽기/쓰기 권한이 있다. |
| PERM-005 | `ls -ld /home/agent-admin/agent-app/api_keys /var/log/agent-app && getfacl /home/agent-admin/agent-app/api_keys /var/log/agent-app` | 그룹이 `agent-core`이고 다른 그룹/기타 사용자 쓰기 권한이 없다. |
| ENV-002 | `env` | 5개 `AGENT_` 환경 변수가 명세 값과 일치한다. |
| DATA-001 | `sudo test -f /home/agent-admin/agent-app/api_keys/t_secret.key && sudo wc -l /home/agent-admin/agent-app/api_keys/t_secret.key` | 키 파일이 있고 1줄이다. 원문 키는 보고서에 노출하지 않는다. |
| APP-001 | `sudo -u agent-admin env ... python3 /home/agent-admin/agent-app/agent_app.py` | Boot Sequence 5단계 `[OK]`와 `Agent READY`가 출력된다. |
| APP-002 | `ss -tulnp` | `0.0.0.0:15034` LISTEN 라인이 보인다. |
| MON-001 | `stat -c '%U %G %a %n' /home/agent-admin/agent-app/bin/monitor.sh && bash -n /home/agent-admin/agent-app/bin/monitor.sh` | owner/group/mode가 `agent-dev agent-core 750`이고 Bash 문법 검사가 통과한다. |
| MON-002 | `/home/agent-admin/agent-app/bin/monitor.sh; echo $?` | 앱 프로세스 정상 시 성공, 비정상 조건에서는 exit `1`이다. |
| MON-003 | `/home/agent-admin/agent-app/bin/monitor.sh; echo $?` | 포트 정상 시 성공, 비정상 조건에서는 exit `1`이다. |
| MON-004 | `/home/agent-admin/agent-app/bin/monitor.sh` | 방화벽 비활성 상태에서 `[WARNING]`만 출력하고 스크립트가 계속된다. |
| MON-005 | `/home/agent-admin/agent-app/bin/monitor.sh` | CPU, MEM, DISK_USED 값이 출력 또는 로그에 포함된다. |
| MON-006 | `/home/agent-admin/agent-app/bin/monitor.sh` | 임계값 초과 조건에서 `[WARNING]`이 출력된다. |
| MON-007 | `sudo tail -n 5 /var/log/agent-app/monitor.log` | 지정 로그 형식의 최근 줄이 보인다. |
| MON-008 | `grep -n '10485760\\|10MB\\|logrotate\\|monitor.log' /home/agent-admin/agent-app/bin/monitor.sh` | `10MB/10개` 유지 로직 또는 설정이 확인된다. |
| CRON-001 | `sudo crontab -u agent-admin -l` | 매분 `monitor.sh` 실행 항목이 보인다. |
| CRON-002 | `sudo wc -l /var/log/agent-app/monitor.log; sleep 70; sudo wc -l /var/log/agent-app/monitor.log` | 1분 뒤 라인 수가 증가한다. |
| DOC-001 | `ls -l submission/` | 수행 내역서 파일이 있고 필수 체크리스트가 포함되어 있다. |
| SUB-001 | `find submission -maxdepth 2 -type f` | 제출용 수행 내역서 1개가 확인된다. |
| SUB-002 | `find submission -path '*monitor.sh' -type f -print` | 제출용 `monitor.sh`가 확인된다. |
| CHECK-001 | `bash scripts/check.sh` | 전체 검증이 실행되고 exit code와 로그가 기록된다. |
| CHECK-002 | `bash scripts/smoke.sh` | 핵심 빠른 점검이 실행되고 exit code와 로그가 기록된다. |
| BONUS-001 | `bash submission/home/agent-admin/agent-app/bin/report.sh` | 평균/최대/최소와 샘플 수가 출력된다. |
| BONUS-002 | `bash submission/home/agent-admin/agent-app/bin/log_retention.sh` | 7일 경과 로그 압축/아카이브 이동과 30일 경과 아카이브 삭제 정책이 동작한다. |
