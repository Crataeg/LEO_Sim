# -*- coding: utf-8 -*-
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import csv
import mat73


ROOT = Path(__file__).resolve().parents[1]
V7_DIR = ROOT / "baseline_snapshot" / "LEO_Sim" / "LEO_Sim" / "LEO_Sim_V7" / "v7proj"
EXPORT_DIR = V7_DIR / "dataset_stft_r2021a" / "_exports"
OUT_DIR = ROOT / "research_notes" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    rs = mat73.loadmat(str(V7_DIR / "outputs_v7" / "result_v7.mat"))["resultSave"]
    sim = rs["simDL_Worst"]
    ps = np.asarray(sim["PS_mW"], dtype=float).reshape(-1)
    pi = np.asarray(sim["PI_mW"], dtype=float).reshape(-1)
    pj = np.asarray(sim["PJ_mW"], dtype=float).reshape(-1)

    rows = []
    for f in sorted(EXPORT_DIR.glob("sim_keyframe_*.png")):
        m = re.search(r"_k(\d+)_([a-z]+)_([a-z]+)\.png$", f.name)
        if not m:
            continue
        k = int(m.group(1)) - 1
        true_lab = m.group(2)
        pred_lab = m.group(3)
        jsr_db = 10 * np.log10(max(pj[k], 1e-12) / max(ps[k], 1e-12))
        isr_db = 10 * np.log10(max(pi[k], 1e-12) / max(ps[k], 1e-12))
        in_training_support = (jsr_db >= 0.0) or (true_lab == "none")
        rows.append(
            {
                "filename": f.name,
                "k": k + 1,
                "true_label": true_lab,
                "pred_label": pred_lab,
                "correct": int(true_lab == pred_lab),
                "jsr_db_pj_over_ps": jsr_db,
                "isr_db_pi_over_ps": isr_db,
                "in_training_support_by_jsr": int(in_training_support),
            }
        )

    out_csv = OUT_DIR / "interference_keyframe_diagnostics.csv"
    with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "filename",
                "k",
                "true_label",
                "pred_label",
                "correct",
                "jsr_db_pj_over_ps",
                "isr_db_pi_over_ps",
                "in_training_support_by_jsr",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    correct = sum(r["correct"] for r in rows)
    total = len(rows)
    acc = correct / max(total, 1)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.2))

    x = np.arange(total)
    jsr = np.array([r["jsr_db_pj_over_ps"] for r in rows])
    isr = np.array([r["isr_db_pi_over_ps"] for r in rows])
    ok = np.array([r["correct"] for r in rows], dtype=bool)

    axes[0].scatter(x[ok], jsr[ok], color="#16a34a", s=60, label="Correct")
    axes[0].scatter(x[~ok], jsr[~ok], color="#dc2626", s=60, label="Wrong")
    axes[0].axhline(0, color="#111827", linestyle="--", linewidth=1.2, label="Train JSR floor")
    axes[0].set_xticks(x, [str(r["k"]) for r in rows], rotation=0)
    axes[0].set_xlabel("Keyframe index k")
    axes[0].set_ylabel("JSR = 10log10(PJ/PS) (dB)")
    axes[0].set_title("Jammer-to-Signal Ratio of Exported Keyframes")
    axes[0].legend(frameon=False, loc="best")

    axes[1].scatter(jsr, isr, c=np.where(ok, "#16a34a", "#dc2626"), s=70)
    for r in rows:
        axes[1].annotate(str(r["k"]), (r["jsr_db_pj_over_ps"], r["isr_db_pi_over_ps"]), fontsize=8, xytext=(4, 2), textcoords="offset points")
    axes[1].axvline(0, color="#111827", linestyle="--", linewidth=1.0)
    axes[1].axhline(0, color="#111827", linestyle="--", linewidth=1.0)
    axes[1].set_xlabel("JSR = 10log10(PJ/PS) (dB)")
    axes[1].set_ylabel("ISR = 10log10(PI/PS) (dB)")
    axes[1].set_title("Most Wrong Samples Are Far Below the Training JSR Range")

    fig.suptitle(f"Interference Keyframe Diagnostics | accuracy={acc:.3f} ({correct}/{total})", fontsize=15, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "interference_keyframe_diagnostics.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
