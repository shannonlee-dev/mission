#!/usr/bin/env bash
set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATTERN="${AGENT_APP_PROCESS_NAME:-agent-app-leak}"
APP_PID="${AGENT_APP_PID:-}"
PORT="${AGENT_PORT:-15034}"
DEFAULT_LOG_DIR="${MONITOR_LOG_DIR:-${AGENT_LOG_DIR:-$SCRIPT_DIR/evidence}}"
LOG_FILE="${MONITOR_LOG_FILE:-$DEFAULT_LOG_DIR/monitor.log}"
MAX_LOG_SIZE="${MONITOR_MAX_LOG_SIZE:-10485760}"
MAX_ROTATED_FILES="${MONITOR_MAX_ROTATED_FILES:-10}"
CPU_SAMPLE_INTERVAL="${MONITOR_CPU_INTERVAL:-1}"

fail() {
  printf '%s\n' "$1"
  exit 1
}

sample_cpu_percent() {
  if [ -n "${MONITOR_CPU_OVERRIDE:-}" ]; then
    printf '%s\n' "$MONITOR_CPU_OVERRIDE"
    return 0
  fi

  read -r _ user1 nice1 system1 idle1 iowait1 irq1 softirq1 steal1 _ < /proc/stat
  total1=$((user1 + nice1 + system1 + idle1 + iowait1 + irq1 + softirq1 + steal1))
  idle_all1=$((idle1 + iowait1))
  sleep "$CPU_SAMPLE_INTERVAL"
  read -r _ user2 nice2 system2 idle2 iowait2 irq2 softirq2 steal2 _ < /proc/stat
  total2=$((user2 + nice2 + system2 + idle2 + iowait2 + irq2 + softirq2 + steal2))
  idle_all2=$((idle2 + iowait2))
  total_delta=$((total2 - total1))
  idle_delta=$((idle_all2 - idle_all1))

  awk -v total="$total_delta" -v idle="$idle_delta" 'BEGIN {
    if (total <= 0) {
      printf "0.0"
    } else {
      printf "%.1f", ((total - idle) / total) * 100
    }
  }'
}

sample_mem_percent() {
  if [ -n "${MONITOR_MEM_OVERRIDE:-}" ]; then
    printf '%s\n' "$MONITOR_MEM_OVERRIDE"
    return 0
  fi

  ps -p "$pid" -o pmem= | awk '{printf "%.1f", $1 + 0}'
}

sample_mem_mb() {
  if [ -n "${MONITOR_MEM_MB_OVERRIDE:-}" ]; then
    printf '%s\n' "$MONITOR_MEM_MB_OVERRIDE"
    return 0
  fi

  ps -p "$pid" -o rss= | awk '{printf "%.1f", ($1 + 0) / 1024}'
}

sample_mem_kb() {
  if [ -r "/proc/$pid/status" ]; then
    awk '/^VmRSS:/ {print $2; exit}' "/proc/$pid/status"
    return 0
  fi
  printf '0'
}

sample_disk_percent() {
  if [ -n "${MONITOR_DISK_OVERRIDE:-}" ]; then
    printf '%s\n' "$MONITOR_DISK_OVERRIDE"
    return 0
  fi

  df / | awk 'NR == 2 {gsub("%", "", $5); print $5}'
}

rotate_logs_if_needed() {
  [ -f "$LOG_FILE" ] || return 0

  current_size="$(stat -c '%s' "$LOG_FILE" 2>/dev/null || printf '0')"
  [ "$current_size" -le "$MAX_LOG_SIZE" ] && return 0

  i=$((MAX_ROTATED_FILES - 1))
  while [ "$i" -ge 1 ]; do
    if [ -f "$LOG_FILE.$i" ]; then
      mv "$LOG_FILE.$i" "$LOG_FILE.$((i + 1))"
    fi
    i=$((i - 1))
  done
  mv "$LOG_FILE" "$LOG_FILE.1"
  : > "$LOG_FILE"

  find "$(dirname "$LOG_FILE")" -maxdepth 1 -type f -name 'monitor.log.*' \
    | sort -Vr \
    | awk -v keep="$MAX_ROTATED_FILES" 'NR > keep {print}' \
    | xargs -r rm -f
}

find_app_pid() {
  if [ -n "$APP_PID" ]; then
    if ps -p "$APP_PID" >/dev/null 2>&1; then
      child_pid="$(
        pgrep -P "$APP_PID" \
          | while read -r child; do
              ps -p "$child" -o rss=,pid= 2>/dev/null
            done \
          | sort -nr \
          | awk 'NR == 1 {print $2}'
      )"
      if [ -n "$child_pid" ]; then
        printf '%s\n' "$child_pid"
        return 0
      fi
      printf '%s\n' "$APP_PID"
      return 0
    fi
    return 1
  fi

  pgrep -u "$(id -u)" -f "$APP_PATTERN" \
    | awk -v self="$$" '$1 != self {print; exit}'
}

pid="$(find_app_pid)"
if [ -z "$pid" ]; then
  fail "Checking process '$APP_PATTERN'... [FAIL]"
fi
port_ok=0
if ss -tuln | awk -v port=":$PORT" '$5 ~ port "$" {found = 1} END {exit found ? 0 : 1}'; then
  port_ok=1
fi
cpu="$(sample_cpu_percent)"
mem="$(sample_mem_percent)"
mem_mb="$(sample_mem_mb)"
mem_kb="$(sample_mem_kb)"
disk="$(sample_disk_percent)"
timestamp="$(date '+%Y-%m-%dT%H:%M:%S')"
line="ts=$timestamp pid=$pid cpu=$cpu mem=$mem rss_mb=$mem_mb disk_used=$disk port=$PORT port_ok=$port_ok"

log_dir="$(dirname "$LOG_FILE")"
if [ ! -d "$log_dir" ]; then
  fail "Log directory does not exist: $log_dir"
fi
if [ ! -w "$log_dir" ]; then
  fail "Log directory is not writable: $log_dir"
fi

rotate_logs_if_needed
printf '%s\n' "$line" >> "$LOG_FILE" \
  || fail "Failed to append log: $LOG_FILE"

printf '%s\n' "$line"
