#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import math
import os
import re
from typing import List, Tuple

LINE_RE = re.compile(
    r"ts=(?P<ts>\S+)\s+pid=(?P<pid>\d+)\s+cpu=(?P<cpu>[0-9.]+)\s+mem=(?P<mem>[0-9.]+)\s+rss_mb=(?P<rss>[0-9.]+)\s+disk_used=(?P<disk>[0-9.]+)\s+port=(?P<port>\d+)\s+port_ok=(?P<port_ok>[01])"
)


def parse_line(line: str) -> Tuple[dt.datetime, float]:
    match = LINE_RE.search(line)
    if not match:
        raise ValueError("unrecognized line format")
    ts = dt.datetime.fromisoformat(match.group("ts"))
    cpu = float(match.group("cpu"))
    return ts, cpu


def compute_rates(samples: List[Tuple[dt.datetime, float]]):
    rows = []
    prev_ts = None
    prev_cpu = None
    for ts, cpu in samples:
        if prev_ts is None:
            rows.append((ts, cpu, 0.0, 0.0, 0.0))
        else:
            delta_t = (ts - prev_ts).total_seconds()
            if delta_t <= 0:
                delta_t = 0.0
            delta_cpu = cpu - prev_cpu
            rate = 0.0 if delta_t == 0 else delta_cpu / delta_t
            rows.append((ts, cpu, delta_cpu, delta_t, rate))
        prev_ts = ts
        prev_cpu = cpu
    return rows


def find_spike_windows(rows, threshold: float):
    windows = []
    current = None
    for ts, cpu, delta_cpu, delta_t, rate in rows:
        if rate >= threshold:
            if current is None:
                current = {
                    "start": ts,
                    "end": ts,
                    "max_rate": rate,
                    "max_cpu": cpu,
                }
            else:
                current["end"] = ts
                current["max_rate"] = max(current["max_rate"], rate)
                current["max_cpu"] = max(current["max_cpu"], cpu)
        else:
            if current is not None:
                windows.append(current)
                current = None
    if current is not None:
        windows.append(current)
    return windows


def write_csv(rows, out_path: str, threshold: float):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu", "delta_cpu", "delta_t", "rate", "is_spike"])
        for ts, cpu, delta_cpu, delta_t, rate in rows:
            writer.writerow(
                [
                    ts.isoformat(),
                    f"{cpu:.2f}",
                    f"{delta_cpu:.2f}",
                    f"{delta_t:.2f}",
                    f"{rate:.2f}",
                    "1" if rate >= threshold else "0",
                ]
            )


def write_report(out_path: str, rows, windows, threshold: float, plot_path: str, csv_path: str):
    total = len(rows)
    spike_count = len(windows)
    with open(out_path, "w") as f:
        f.write("# CPU Spike Analysis\n\n")
        f.write("## Summary\n")
        f.write(f"- Samples: {total}\n")
        f.write(f"- Spike windows: {spike_count}\n")
        f.write(f"- Threshold: {threshold:.2f} %/s\n\n")
        f.write("## Method\n")
        f.write("- Based on dense sampling with monitor.sh and first-order finite difference (delta CPU / delta t).\n")
        f.write("- This is numeric differentiation on discrete samples, not a continuous derivative.\n\n")
        f.write("## Outputs\n")
        f.write(f"- CSV: {csv_path}\n")
        if plot_path:
            f.write(f"- Plot: {plot_path}\n")
        f.write("\n")
        f.write("## Spike Windows\n")
        if not windows:
            f.write("- No spike windows detected.\n")
            return
        for idx, window in enumerate(windows, 1):
            start = window["start"].isoformat()
            end = window["end"].isoformat()
            f.write(
                f"- Window {idx}: {start} -> {end}, max_rate={window['max_rate']:.2f} %/s, max_cpu={window['max_cpu']:.2f}%\n"
            )


def try_plot(rows, out_path: str, threshold: float):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False

    timestamps = [r[0] for r in rows]
    cpu_vals = [r[1] for r in rows]
    rate_vals = [r[4] for r in rows]

    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(timestamps, cpu_vals, color="#1f77b4", label="CPU (%)", linewidth=1.5)
    ax1.set_ylabel("CPU (%)")
    ax1.set_xlabel("Time")

    ax2 = ax1.twinx()
    ax2.plot(timestamps, rate_vals, color="#d62728", label="dCPU/dt (%/s)", linewidth=1.0, alpha=0.7)
    ax2.axhline(threshold, color="#d62728", linestyle="--", linewidth=1.0, alpha=0.6)
    ax2.set_ylabel("dCPU/dt (%/s)")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return True


def main():
    parser = argparse.ArgumentParser(description="Analyze CPU spike windows from monitor.sh logs.")
    parser.add_argument("--input", required=True, help="Input monitor_cpu.log")
    parser.add_argument("--csv", required=True, help="Output CSV path")
    parser.add_argument("--report", required=True, help="Output Markdown report path")
    parser.add_argument("--plot", required=True, help="Output PNG path")
    parser.add_argument("--threshold", type=float, default=10.0, help="Spike threshold in %/s")

    args = parser.parse_args()

    samples = []
    with open(args.input, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(parse_line(line))
            except ValueError:
                continue

    if len(samples) < 2:
        raise SystemExit("Not enough samples to analyze.")

    rows = compute_rates(samples)
    windows = find_spike_windows(rows, args.threshold)

    os.makedirs(os.path.dirname(args.csv), exist_ok=True)
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    os.makedirs(os.path.dirname(args.plot), exist_ok=True)

    write_csv(rows, args.csv, args.threshold)
    plot_ok = try_plot(rows, args.plot, args.threshold)
    write_report(args.report, rows, windows, args.threshold, args.plot if plot_ok else "", args.csv)

    print(f"[OK] CSV: {args.csv}")
    if plot_ok:
        print(f"[OK] Plot: {args.plot}")
    else:
        print("[WARN] Plot skipped (matplotlib not available)")
    print(f"[OK] Report: {args.report}")


if __name__ == "__main__":
    main()
