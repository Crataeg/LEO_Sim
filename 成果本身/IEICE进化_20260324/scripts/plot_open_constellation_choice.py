# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "downloads" / "constellation_data"
FIG_DIR = ROOT / "research_notes" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

MU_KM3_S2 = 398600.4418
RE_KM = 6378.137


def mean_altitude_km(mean_motion_rev_per_day: float) -> float:
    n_rad_s = mean_motion_rev_per_day * 2.0 * math.pi / 86400.0
    a_km = (MU_KM3_S2 / (n_rad_s ** 2)) ** (1.0 / 3.0)
    return a_km - RE_KM


def load_json_file(name: str):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def load_csv_rows(name: str):
    with (DATA_DIR / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_points(rows, inclination_key="INCLINATION", mm_key="MEAN_MOTION"):
    incl = np.array([float(x[inclination_key]) for x in rows], dtype=float)
    alt = np.array([mean_altitude_km(float(x[mm_key])) for x in rows], dtype=float)
    return incl, alt


def main() -> None:
    starlink = load_json_file("celestrak_starlink_gp.json")
    oneweb = load_json_file("celestrak_oneweb_gp.json")
    qianfan = load_json_file("celestrak_qianfan_gp.json")
    geesat = load_csv_rows("celestrak_geesat_subset.csv")

    series = [
        ("Starlink", "#2563eb", 5, 0.30, *get_points(starlink)),
        ("OneWeb", "#dc2626", 18, 0.55, *get_points(oneweb)),
        ("Qianfan", "#16a34a", 22, 0.65, *get_points(qianfan)),
        ("GeeSat", "#f59e0b", 26, 0.70, *get_points(geesat)),
    ]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.4))

    for label, color, size, alpha, incl, alt in series:
        axes[0].scatter(incl, alt, s=size, alpha=alpha, color=color, label=f"{label} ({len(incl)})")
    axes[0].set_xlabel("Inclination (deg)")
    axes[0].set_ylabel("Approx. Mean Altitude (km)")
    axes[0].set_title("Open Constellation Data Comparison")
    axes[0].legend(frameon=False, loc="best")

    labels = [x[0] for x in series]
    counts = [len(x[4]) for x in series]
    mean_alt = [float(np.mean(x[5])) for x in series]
    x = np.arange(len(labels))
    width = 0.36
    ax2 = axes[1]
    ax2.bar(x - width / 2, counts, width, color="#60a5fa", label="Satellite count")
    ax2.set_ylabel("Satellite Count")
    ax2.set_xticks(x, labels)
    ax2.set_title("Count vs Mean Altitude")
    ax2.grid(True, axis="y", alpha=0.20)

    ax2b = ax2.twinx()
    ax2b.plot(x, mean_alt, color="#111827", marker="o", linewidth=2.0, label="Mean altitude")
    ax2b.set_ylabel("Mean Altitude (km)")

    fig.suptitle("Which Open Constellation Data Is Best for the Current Project?", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "open_constellation_choice_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
