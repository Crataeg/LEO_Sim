# -*- coding: utf-8 -*-
from pathlib import Path
import json
import math
import csv

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


def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def mean_altitude_km(mean_motion_rev_per_day: float) -> float:
    n_rad_s = mean_motion_rev_per_day * 2.0 * math.pi / 86400.0
    a_km = (MU_KM3_S2 / (n_rad_s ** 2)) ** (1.0 / 3.0)
    return a_km - RE_KM


def shell_summary(objects, label: str):
    incl = np.array([float(x["INCLINATION"]) for x in objects], dtype=float)
    mm = np.array([float(x["MEAN_MOTION"]) for x in objects], dtype=float)
    alt = np.array([mean_altitude_km(v) for v in mm], dtype=float)

    bins = {}
    for i, a in zip(incl, alt):
        key = (round(i, 1), round(a / 10.0) * 10)
        bins[key] = bins.get(key, 0) + 1

    top_shells = sorted(bins.items(), key=lambda x: x[1], reverse=True)[:8]
    rows = []
    for (inc_key, alt_key), count in top_shells:
        rows.append(
            {
                "constellation": label,
                "inclination_deg_rounded": inc_key,
                "mean_altitude_km_rounded10": alt_key,
                "count": count,
            }
        )
    return incl, alt, rows


def main() -> None:
    starlink = load_json("celestrak_starlink_gp.json")
    oneweb = load_json("celestrak_oneweb_gp.json")

    incl_s, alt_s, rows_s = shell_summary(starlink, "Starlink")
    incl_o, alt_o, rows_o = shell_summary(oneweb, "OneWeb")

    plt.style.use("seaborn-v0_8-whitegrid")

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2))
    axes[0].scatter(incl_s, alt_s, s=6, alpha=0.35, color="#2563eb", label=f"Starlink ({len(starlink)})")
    axes[0].scatter(incl_o, alt_o, s=16, alpha=0.55, color="#dc2626", label=f"OneWeb ({len(oneweb)})")
    axes[0].set_xlabel("Inclination (deg)")
    axes[0].set_ylabel("Approx. Mean Altitude (km)")
    axes[0].set_title("Constellation Shell Distribution")
    axes[0].legend(frameon=False, loc="best")

    bins = np.arange(300, 1501, 25)
    axes[1].hist(alt_s, bins=bins, color="#2563eb", alpha=0.55, label="Starlink")
    axes[1].hist(alt_o, bins=bins, color="#dc2626", alpha=0.55, label="OneWeb")
    axes[1].set_xlabel("Approx. Mean Altitude (km)")
    axes[1].set_ylabel("Satellite Count")
    axes[1].set_title("Altitude Histogram")
    axes[1].legend(frameon=False, loc="best")

    fig.suptitle("Open Constellation Data from CelesTrak", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "constellation_shell_overview.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    with (FIG_DIR / "constellation_shell_summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "constellation",
                "inclination_deg_rounded",
                "mean_altitude_km_rounded10",
                "count",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_s + rows_o)

    note = ROOT / "research_notes" / "constellation_data_integration_note.md"
    note.write_text(
        "\n".join(
            [
                "# Constellation Data Integration Note",
                "",
                "Current step:",
                "- Downloaded open GP/TLE data from the official CelesTrak interface.",
                "- Generated an initial shell distribution plot using Starlink and OneWeb current orbital data.",
                "",
                "Why this matters for the IEICE direction:",
                "- It turns the platform from a purely self-defined simulation scene into a data-informed scenario.",
                "- It enables figures based on real constellation shells, not only synthetic 12x8 orbital settings.",
                "- It supports later additions such as visible-satellite counts over Qingdao/Beijing, access windows, and constellation-aware interference cases.",
                "",
                "Current limitations:",
                "- The present plot only uses GP-derived orbital elements, not high-precision ephemeris propagation.",
                "- Gateway and beam data are not yet included.",
                "- The current platform logic is still synthetic and has not yet been coupled to these real shells.",
                "",
                "Next recommended step:",
                "- Replace the fixed 12x8 shell in one branch of the engineering code with a Starlink/OneWeb subset built from open GP data.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(FIG_DIR / "constellation_shell_overview.png")
    print(FIG_DIR / "constellation_shell_summary.csv")


if __name__ == "__main__":
    main()
