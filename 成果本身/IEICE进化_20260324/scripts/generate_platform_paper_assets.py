# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import logging
import shutil

import mat73
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


SOURCE_V7 = Path(r"D:\论文卫星\成果本身\代码工程\LEO_Sim\LEO_Sim\LEO_Sim_V7\v7proj")
RESULT_FILE = SOURCE_V7 / "outputs_v7" / "result_v7.mat"
SUMMARY_FILE = SOURCE_V7 / "outputs_v7" / "summary_v7.txt"
SOURCE_EXPORTS = SOURCE_V7 / "dataset_stft_r2021a" / "_exports"
OUTPUT_DIR = Path(__file__).resolve().parent

LINK_KEYS = [
    ("DL", "simDL_Base", "simDL_Worst"),
    ("UL", "simUL_Base", "simUL_Worst"),
    ("E2E", "simE2E_Base", "simE2E_Worst"),
]


def arr(value):
    return np.asarray(value, dtype=float).reshape(-1)


def scalar(value):
    return float(np.asarray(value, dtype=float).reshape(-1)[0])


def match_length(value, length):
    value = np.asarray(value, dtype=float).reshape(-1)
    if value.size == length:
        return value
    if value.size == 1:
        return np.full(length, float(value[0]), dtype=float)
    raise ValueError(f"Cannot broadcast array of length {value.size} to {length}")


def mw_to_dbm(value):
    value = np.maximum(np.asarray(value, dtype=float), 1e-30)
    return 10.0 * np.log10(value)


def compute_case_stats(sim, threshold_mbps, sample_time_s):
    thr = arr(sim["THR"])
    sinr = arr(sim["SINR"])
    bler = arr(sim["BLER"])
    delay_key = "Delay_ms" if "Delay_ms" in sim else "E2Ems"
    delay = arr(sim[delay_key])
    outage_mask = thr < threshold_mbps
    return {
        "mean_throughput_mbps": float(np.nanmean(thr)),
        "outage_fraction": float(np.mean(outage_mask)),
        "outage_minutes": float(np.sum(outage_mask) * sample_time_s / 60.0),
        "min_throughput_mbps": float(np.nanmin(thr)),
        "p05_throughput_mbps": float(np.nanpercentile(thr, 5)),
        "mean_sinr_db": float(np.nanmean(sinr)),
        "min_sinr_db": float(np.nanmin(sinr)),
        "mean_bler": float(np.nanmean(bler)),
        "mean_delay_ms": float(np.nanmean(delay)),
        "max_delay_ms": float(np.nanmax(delay)),
    }


def write_metrics_csv(rs, sample_time_s, threshold_mbps):
    output_csv = OUTPUT_DIR / "paper_metrics_summary.csv"
    header = [
        "link",
        "case",
        "mean_throughput_mbps",
        "outage_fraction",
        "outage_minutes",
        "min_throughput_mbps",
        "p05_throughput_mbps",
        "mean_sinr_db",
        "min_sinr_db",
        "mean_bler",
        "mean_delay_ms",
        "max_delay_ms",
    ]
    rows = []
    for link_name, base_key, worst_key in LINK_KEYS:
        rows.append({"link": link_name, "case": "Base", **compute_case_stats(rs[base_key], threshold_mbps, sample_time_s)})
        rows.append({"link": link_name, "case": "Worst", **compute_case_stats(rs[worst_key], threshold_mbps, sample_time_s)})
    with output_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    return output_csv


def copy_reference_assets():
    copies = {
        "summary_v7.txt": SUMMARY_FILE,
        "stft_confusion_test.png": SOURCE_EXPORTS / "confusion_test.png",
        "stft_keyframes_montage.png": SOURCE_EXPORTS / "sim_keyframes_montage.png",
        "stft_train_montage.png": SOURCE_EXPORTS / "montage_train.png",
    }
    for target_name, source_file in copies.items():
        shutil.copy2(source_file, OUTPUT_DIR / target_name)


def add_box(ax, x, y, w, h, title, body, fc, ec="#1f2937"):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.4,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.70, title, ha="center", va="center", fontsize=11, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.38, body, ha="center", va="center", fontsize=9, wrap=True)


def add_arrow(ax, start, end):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.4, color="#374151")
    ax.add_patch(arrow)


def plot_architecture_figure(project_name):
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, 0.04, 0.60, 0.20, 0.22, "Scenario & Geometry", "satelliteScenario\nLEO constellation\nuser / gateway / jammer", "#dbeafe")
    add_box(ax, 0.29, 0.60, 0.20, 0.22, "Power Precompute", "DL / UL signal power\nCCI, jammer, noise\nrouting graph", "#dcfce7")
    add_box(ax, 0.54, 0.60, 0.18, 0.22, "Link Solver", "simulateStarNetV7\nSINR, THR, BLER\nDoppler, delay", "#fee2e2")
    add_box(ax, 0.77, 0.60, 0.18, 0.22, "Outputs", "result_v7.mat\nsummary_v7.txt\ncompliance rows", "#fef3c7")

    add_box(ax, 0.24, 0.18, 0.22, 0.22, "Worst-Case Search", "InfoGAN jammer envelope\nGA search on z + c + scale", "#ede9fe")
    add_box(ax, 0.56, 0.18, 0.22, 0.22, "Interference ID", "power -> IQ snapshot\nSTFT image\nLeNet classifier", "#fae8ff")

    add_arrow(ax, (0.24, 0.71), (0.29, 0.71))
    add_arrow(ax, (0.49, 0.71), (0.54, 0.71))
    add_arrow(ax, (0.72, 0.71), (0.77, 0.71))
    add_arrow(ax, (0.35, 0.40), (0.35, 0.58))
    add_arrow(ax, (0.67, 0.40), (0.63, 0.58))
    add_arrow(ax, (0.46, 0.29), (0.56, 0.29))

    ax.text(0.5, 0.93, "LEO Satellite EMC Simulation Platform (V7)", ha="center", va="center", fontsize=18, fontweight="bold")
    ax.text(0.5, 0.88, project_name, ha="center", va="center", fontsize=11, color="#4b5563")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "01_platform_architecture.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_summary_bars(rs, threshold_mbps):
    labels = [k[0] for k in LINK_KEYS]
    base_mean = [scalar(rs[base_key]["meanThr"]) for _, base_key, _ in LINK_KEYS]
    worst_mean = [scalar(rs[worst_key]["meanThr"]) for _, _, worst_key in LINK_KEYS]
    base_out = [scalar(rs[base_key]["outageFrac"]) * 100 for _, base_key, _ in LINK_KEYS]
    worst_out = [scalar(rs[worst_key]["outageFrac"]) * 100 for _, _, worst_key in LINK_KEYS]

    x = np.arange(len(labels))
    width = 0.34

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2))

    axes[0].bar(x - width / 2, base_mean, width, label="Baseline", color="#2563eb")
    axes[0].bar(x + width / 2, worst_mean, width, label="Worst-case", color="#dc2626")
    axes[0].axhline(threshold_mbps, color="#111827", linestyle="--", linewidth=1.2, label="Outage threshold")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("Mean Throughput (Mbps)")
    axes[0].set_title("Average Throughput")
    axes[0].legend(frameon=False, loc="upper right")

    axes[1].bar(x - width / 2, base_out, width, label="Baseline", color="#60a5fa")
    axes[1].bar(x + width / 2, worst_out, width, label="Worst-case", color="#f87171")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("Outage Ratio (%)")
    axes[1].set_title("Outage under 20 Mbps Constraint")

    for ax in axes:
        ax.grid(True, axis="y", alpha=0.25)
        ax.set_axisbelow(True)

    fig.suptitle("Platform-Level Performance Summary", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02_link_summary_bars.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_throughput_timeseries(rs, sample_time_s, threshold_mbps):
    jam = arr(rs["jamAggWorst"])
    time_min = np.arange(jam.size) * sample_time_s / 60.0

    fig, axes = plt.subplots(3, 1, figsize=(13.5, 10), sharex=True)
    for ax, (label, base_key, worst_key) in zip(axes, LINK_KEYS):
        base_thr = arr(rs[base_key]["THR"])
        worst_thr = arr(rs[worst_key]["THR"])
        ax.plot(time_min, base_thr, color="#2563eb", linewidth=1.8, label=f"{label} baseline")
        ax.plot(time_min, worst_thr, color="#dc2626", linewidth=1.8, label=f"{label} worst-case")
        ax.axhline(threshold_mbps, color="#111827", linestyle="--", linewidth=1.0)
        ax.set_ylabel(f"{label} THR\n(Mbps)")
        ax.grid(True, alpha=0.22)
        ax.legend(frameon=False, loc="upper right")

        twin = ax.twinx()
        twin.fill_between(time_min, jam, color="#9ca3af", alpha=0.20)
        twin.plot(time_min, jam, color="#6b7280", linewidth=1.0)
        twin.set_ylim(0, 1.0)
        twin.set_ylabel("Jam env.", color="#6b7280")
        twin.tick_params(axis="y", colors="#6b7280")

    axes[0].set_title("Throughput Trajectories with Worst-Case Jammer Envelope", fontsize=16, fontweight="bold")
    axes[-1].set_xlabel("Simulation Time (min)")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03_throughput_timeseries.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_power_breakdown(rs, sample_time_s):
    time_min = np.arange(arr(rs["simDL_Worst"]["THR"]).size) * sample_time_s / 60.0
    time_len = time_min.size
    fig, axes = plt.subplots(2, 1, figsize=(13.5, 8.8), sharex=True)

    for ax, label, sim_key in [
        (axes[0], "Downlink Worst-Case", "simDL_Worst"),
        (axes[1], "Uplink Worst-Case", "simUL_Worst"),
    ]:
        sim = rs[sim_key]
        ax.plot(time_min, mw_to_dbm(arr(sim["PS_mW"])), label="Signal", color="#16a34a", linewidth=1.7)
        ax.plot(time_min, mw_to_dbm(arr(sim["PI_mW"])), label="CCI", color="#2563eb", linewidth=1.4)
        ax.plot(time_min, mw_to_dbm(arr(sim["PJ_mW"])), label="Jammer", color="#dc2626", linewidth=1.4)
        ax.plot(time_min, mw_to_dbm(match_length(sim["Pn_mW"], time_len)), label="Noise", color="#7c3aed", linewidth=1.4)
        ax.set_ylabel("Power (dBm)")
        ax.set_title(label)
        ax.grid(True, alpha=0.22)
        ax.legend(frameon=False, ncol=4, loc="upper right")

    axes[-1].set_xlabel("Simulation Time (min)")
    fig.suptitle("Signal / Interference / Jammer / Noise Decomposition", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "04_power_breakdown_worst.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_jammer_outage(rs, sample_time_s, threshold_mbps):
    jam = arr(rs["jamAggWorst"])
    time_min = np.arange(jam.size) * sample_time_s / 60.0

    fig, axes = plt.subplots(2, 1, figsize=(13.5, 7.5), sharex=True)

    axes[0].plot(time_min, jam, color="#4b5563", linewidth=1.8)
    axes[0].fill_between(time_min, jam, color="#9ca3af", alpha=0.25)
    axes[0].axhline(0.5, color="#111827", linestyle="--", linewidth=1.0)
    axes[0].set_ylabel("Normalized Envelope")
    axes[0].set_title("Best Jammer Envelope from InfoGAN + GA")
    axes[0].grid(True, alpha=0.22)

    offsets = {"DL": 2.0, "UL": 1.0, "E2E": 0.0}
    colors = {"DL": "#2563eb", "UL": "#dc2626", "E2E": "#16a34a"}
    for label, _, worst_key in LINK_KEYS:
        thr = arr(rs[worst_key]["THR"])
        outage = (thr < threshold_mbps).astype(float)
        axes[1].step(time_min, outage + offsets[label], where="post", color=colors[label], linewidth=1.6, label=label)

    axes[1].set_yticks([0.0, 1.0, 2.0, 3.0], ["E2E off", "UL off", "DL off", ""])
    axes[1].set_ylim(-0.1, 3.1)
    axes[1].set_ylabel("Outage State")
    axes[1].set_xlabel("Simulation Time (min)")
    axes[1].set_title("Outage Windows under Worst-Case Search")
    axes[1].grid(True, alpha=0.22)
    axes[1].legend(frameon=False, ncol=3, loc="upper right")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "05_jammer_outage_windows.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main():
    plt.style.use("seaborn-v0_8-whitegrid")
    logging.getLogger().setLevel(logging.CRITICAL)
    result = mat73.loadmat(RESULT_FILE)
    rs = result["resultSave"]

    sample_time_s = scalar(rs["cfg"]["Time"]["SampleTime_s"])
    threshold_mbps = scalar(rs["cfg"]["Requirements"]["MinThr_Mbps"])
    project_name = "Vehicle-Mounted LEO Satellite EMC Forward Design | V7.0"

    copy_reference_assets()
    write_metrics_csv(rs, sample_time_s, threshold_mbps)
    plot_architecture_figure(project_name)
    plot_summary_bars(rs, threshold_mbps)
    plot_throughput_timeseries(rs, sample_time_s, threshold_mbps)
    plot_power_breakdown(rs, sample_time_s)
    plot_jammer_outage(rs, sample_time_s, threshold_mbps)


if __name__ == "__main__":
    main()
