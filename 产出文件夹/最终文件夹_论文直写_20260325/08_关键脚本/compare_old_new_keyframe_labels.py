# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mat73
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
V7_DIR = ROOT / "02_基线快照" / "LEO_Sim" / "LEO_Sim" / "LEO_Sim_V7" / "v7proj"
OUT_DIR = ROOT / "06_识别模块问题与改进"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    exports = V7_DIR / "dataset_stft_r2021a" / "_exports"
    rs = mat73.loadmat(str(V7_DIR / "outputs_v7" / "result_v7.mat"))["resultSave"]
    sim = rs["simDL_Worst"]
    ps = np.asarray(sim["PS_mW"], dtype=float).reshape(-1)
    pi = np.asarray(sim["PI_mW"], dtype=float).reshape(-1)
    pj = np.asarray(sim["PJ_mW"], dtype=float).reshape(-1)
    pn = np.asarray(sim["Pn_mW"], dtype=float).reshape(-1)
    if pn.size == 1:
        pn = np.full_like(ps, float(pn[0]))

    rows = []
    old_correct = 0
    new_correct = 0
    for f in sorted(exports.glob("sim_keyframe_*.png")):
        m = re.search(r"_k(\d+)_([a-z]+)_([a-z]+)\.png$", f.name)
        if not m:
            continue

        k = int(m.group(1)) - 1
        old_true = m.group(2)
        pred = m.group(3)

        ps_k = max(ps[k], 1e-12)
        pi_k = max(pi[k], 1e-12)
        pj_k = max(pj[k], 1e-12)
        pn_k = max(pn[k], 1e-12)

        jsr = 10 * np.log10(pj_k / ps_k)
        isr = 10 * np.log10(pi_k / ps_k)
        inr = 10 * np.log10(max(pi_k, pj_k) / pn_k)

        if inr < 3.0 or (jsr < -10.0 and isr < -8.0):
            new_true = "none"
        else:
            if pj_k >= pi_k and jsr >= -10.0:
                new_true = old_true if old_true in ["tone", "pbnj", "mod"] else "tone"
            else:
                new_true = "mod"

        old_ok = int(old_true == pred)
        new_ok = int(new_true == pred)
        old_correct += old_ok
        new_correct += new_ok

        rows.append(
            {
                "filename": f.name,
                "k": k + 1,
                "old_true": old_true,
                "new_true": new_true,
                "pred": pred,
                "old_correct": old_ok,
                "new_correct": new_ok,
                "jsr_db": jsr,
                "isr_db": isr,
                "inr_db": inr,
            }
        )

    with (OUT_DIR / "keyframe_old_vs_new_labels.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["filename", "k", "old_true", "new_true", "pred", "old_correct", "new_correct", "jsr_db", "isr_db", "inr_db"],
        )
        writer.writeheader()
        writer.writerows(rows)

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    labels = ["Old keyframe labels", "New hierarchical labels"]
    values = [old_correct / len(rows), new_correct / len(rows)]
    bars = ax.bar(labels, values, color=["#dc2626", "#16a34a"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Accuracy")
    ax.set_title("Keyframe Accuracy Before vs After Hierarchical Label Rule")
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.3f}", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "keyframe_old_vs_new_labels.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
