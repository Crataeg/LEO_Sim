from __future__ import annotations

import json
import shutil
from pathlib import Path

import h5py
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent.parent
SOURCE_DIR = (
    REPO_ROOT
    / "产出文件夹"
    / "卫星仿真平台工程文件夹_最终版"
    / "LEO_Sim"
    / "LEO_Sim"
    / "LEO_Sim_V7"
    / "v7proj"
    / "outputs_v7"
)
RESULT_PATH = SOURCE_DIR / "result_v7.mat"
SUMMARY_PATH = SOURCE_DIR / "summary_v7.txt"
PLOTS_DIR = THIS_DIR / "plots"


def _vec(group: h5py.Group, key: str) -> np.ndarray:
    return np.asarray(group[key], dtype=float).reshape(-1)


def _scalar(group: h5py.Group, key: str) -> float:
    return float(np.asarray(group[key]).reshape(-1)[0])


def _flag(group: h5py.Group, key: str) -> bool:
    return bool(int(np.asarray(group[key]).reshape(-1)[0]))


def _matlab_str(group: h5py.Group, key: str) -> str:
    arr = np.asarray(group[key]).astype(np.uint16).reshape(-1, order="F")
    return "".join(chr(int(ch)) for ch in arr if int(ch) != 0)


def _dbm(mw: np.ndarray) -> np.ndarray:
    return 10.0 * np.log10(np.clip(np.asarray(mw, dtype=float), 1e-30, None))


def _pct(x: float) -> float:
    return 100.0 * float(x)


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def load_result() -> tuple[dict[str, object], str]:
    if not RESULT_PATH.exists():
        raise FileNotFoundError(f"Missing result file: {RESULT_PATH}")
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(f"Missing summary file: {SUMMARY_PATH}")

    summary_text = SUMMARY_PATH.read_text(encoding="utf-8", errors="replace")

    with h5py.File(RESULT_PATH, "r") as f:
        result = f["resultSave"]
        cfg = result["cfg"]
        cfg_time = cfg["Time"]
        cfg_const = cfg["Constellation"]
        cfg_jammer = cfg["Jammer"]
        cfg_req = cfg["Requirements"]
        cfg_wc = cfg["WorstCase"]
        cfg_clf = cfg["Classifier"]
        cfg_general = cfg["General"]

        data: dict[str, object] = {
            "project_name": _matlab_str(cfg_general, "ProjectName"),
            "startup_mode": _matlab_str(cfg_general, "StartupMode"),
            "worst_target": _matlab_str(cfg_wc, "Target"),
            "sample_time_s": _scalar(cfg_time, "SampleTime_s"),
            "sim_duration_s_cfg": _scalar(cfg_time, "SimDuration_s"),
            "num_planes": int(_scalar(cfg_const, "NumPlanes")),
            "sats_per_plane": int(_scalar(cfg_const, "SatsPerPlane")),
            "num_jammers": int(_scalar(cfg_jammer, "NumJammers")),
            "min_thr_mbps": _scalar(cfg_req, "MinThr_Mbps"),
            "min_sinr_db": _scalar(cfg_req, "MinSINR_dB"),
            "worst_case_enabled": _flag(cfg_wc, "Enable"),
            "classifier_enabled": _flag(cfg_clf, "Enable"),
            "jam_scale_best_db": _scalar(result, "JamScaleBest_dB"),
            "jam_info_code": _vec(result["simDL_Worst"], "JamInfoCode").tolist(),
        }

        sim_names = [
            "simDL_Base",
            "simDL_Worst",
            "simUL_Base",
            "simUL_Worst",
            "simE2E_Base",
            "simE2E_Worst",
        ]
        sims: dict[str, dict[str, np.ndarray | float]] = {}
        for name in sim_names:
            g = result[name]
            entry: dict[str, np.ndarray | float] = {
                "THR": _vec(g, "THR"),
                "BLER": _vec(g, "BLER"),
                "Serving": _vec(g, "Serving"),
                "Gateway": _vec(g, "Gateway"),
                "meanThr": _scalar(g, "meanThr"),
                "outageFrac": _scalar(g, "outageFrac"),
            }
            if "SINR" in g:
                entry["SINR"] = _vec(g, "SINR")
            if "DopRate_Hzps" in g:
                entry["DopRate_Hzps"] = _vec(g, "DopRate_Hzps")
            if "Delay_ms" in g:
                entry["Delay_ms"] = _vec(g, "Delay_ms")
            if "E2Ems" in g:
                entry["E2Ems"] = _vec(g, "E2Ems")
            if "PS_mW" in g:
                entry["PS_mW"] = _vec(g, "PS_mW")
            if "PI_mW" in g:
                entry["PI_mW"] = _vec(g, "PI_mW")
            if "PJ_mW" in g:
                entry["PJ_mW"] = _vec(g, "PJ_mW")
            if "Prx_dBm" in g:
                entry["Prx_dBm"] = _vec(g, "Prx_dBm")
            sims[name] = entry

        data["sims"] = sims
        n_steps = len(sims["simDL_Base"]["THR"])  # type: ignore[index]
        data["n_steps"] = n_steps
        data["orbit_minutes"] = (n_steps - 1) * data["sample_time_s"] / 60.0  # type: ignore[operator]

    return data, summary_text


def make_stage_overview(data: dict[str, object]) -> None:
    labels = ["DL", "UL", "E2E"]
    base_means = [
        data["sims"]["simDL_Base"]["meanThr"],  # type: ignore[index]
        data["sims"]["simUL_Base"]["meanThr"],  # type: ignore[index]
        data["sims"]["simE2E_Base"]["meanThr"],  # type: ignore[index]
    ]
    worst_means = [
        data["sims"]["simDL_Worst"]["meanThr"],  # type: ignore[index]
        data["sims"]["simUL_Worst"]["meanThr"],  # type: ignore[index]
        data["sims"]["simE2E_Worst"]["meanThr"],  # type: ignore[index]
    ]
    base_outage = [
        _pct(data["sims"]["simDL_Base"]["outageFrac"]),  # type: ignore[index]
        _pct(data["sims"]["simUL_Base"]["outageFrac"]),  # type: ignore[index]
        _pct(data["sims"]["simE2E_Base"]["outageFrac"]),  # type: ignore[index]
    ]
    worst_outage = [
        _pct(data["sims"]["simDL_Worst"]["outageFrac"]),  # type: ignore[index]
        _pct(data["sims"]["simUL_Worst"]["outageFrac"]),  # type: ignore[index]
        _pct(data["sims"]["simE2E_Worst"]["outageFrac"]),  # type: ignore[index]
    ]

    x = np.arange(len(labels))
    width = 0.34

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    axes[0].bar(x - width / 2, base_means, width=width, label="Baseline", color="#4C78A8")
    axes[0].bar(x + width / 2, worst_means, width=width, label="Worst-Case", color="#E45756")
    axes[0].axhline(data["min_thr_mbps"], color="#777777", linestyle="--", linewidth=1.2, label="Min Throughput")  # type: ignore[arg-type]
    axes[0].set_ylabel("Mean Throughput (Mbps)")
    axes[0].set_title("V7 Engineering Throughput Snapshot")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend()

    axes[1].bar(x - width / 2, base_outage, width=width, label="Baseline", color="#72B7B2")
    axes[1].bar(x + width / 2, worst_outage, width=width, label="Worst-Case", color="#F58518")
    axes[1].set_ylabel("Outage (%)")
    axes[1].set_xticks(x, labels)
    axes[1].set_title("Outage Comparison")
    axes[1].grid(True, alpha=0.25)

    _save(fig, "00_stage_overview.png")


def make_throughput_timeseries(data: dict[str, object]) -> None:
    t_min = np.arange(data["n_steps"]) * data["sample_time_s"] / 60.0  # type: ignore[operator]
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    panels = [
        ("DL", "simDL_Base", "simDL_Worst"),
        ("UL", "simUL_Base", "simUL_Worst"),
        ("E2E", "simE2E_Base", "simE2E_Worst"),
    ]
    for ax, (title, base_key, worst_key) in zip(axes, panels):
        ax.plot(t_min, data["sims"][base_key]["THR"], label=f"{title} Baseline", color="#4C78A8")  # type: ignore[index]
        ax.plot(t_min, data["sims"][worst_key]["THR"], label=f"{title} Worst-Case", color="#E45756", alpha=0.95)  # type: ignore[index]
        ax.axhline(data["min_thr_mbps"], color="#777777", linestyle="--", linewidth=1.0)  # type: ignore[arg-type]
        ax.set_ylabel("Mbps")
        ax.set_title(f"{title} Throughput")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right")
    axes[-1].set_xlabel("Time (min)")
    _save(fig, "01_throughput_timeseries.png")


def make_sinr_timeseries(data: dict[str, object]) -> None:
    t_min = np.arange(data["n_steps"]) * data["sample_time_s"] / 60.0  # type: ignore[operator]
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    panels = [
        ("DL", "simDL_Base", "simDL_Worst"),
        ("UL", "simUL_Base", "simUL_Worst"),
    ]
    for ax, (title, base_key, worst_key) in zip(axes, panels):
        ax.plot(t_min, data["sims"][base_key]["SINR"], label=f"{title} Baseline", color="#54A24B")  # type: ignore[index]
        ax.plot(t_min, data["sims"][worst_key]["SINR"], label=f"{title} Worst-Case", color="#EECA3B", alpha=0.95)  # type: ignore[index]
        ax.axhline(data["min_sinr_db"], color="#777777", linestyle="--", linewidth=1.0)  # type: ignore[arg-type]
        ax.set_ylabel("SINR (dB)")
        ax.set_title(f"{title} SINR")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right")
    axes[-1].set_xlabel("Time (min)")
    _save(fig, "02_sinr_timeseries.png")


def make_e2e_quality(data: dict[str, object]) -> None:
    t_min = np.arange(data["n_steps"]) * data["sample_time_s"] / 60.0  # type: ignore[operator]
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(t_min, data["sims"]["simE2E_Base"]["BLER"], label="E2E Baseline", color="#72B7B2")  # type: ignore[index]
    axes[0].plot(t_min, data["sims"]["simE2E_Worst"]["BLER"], label="E2E Worst-Case", color="#F58518")  # type: ignore[index]
    axes[0].set_ylabel("BLER")
    axes[0].set_title("E2E BLER")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend(loc="upper right")

    delay_base = data["sims"]["simDL_Base"]["E2Ems"] if "E2Ems" in data["sims"]["simDL_Base"] else np.zeros(data["n_steps"])  # type: ignore[index]
    delay_worst = data["sims"]["simDL_Worst"]["E2Ems"] if "E2Ems" in data["sims"]["simDL_Worst"] else np.zeros(data["n_steps"])  # type: ignore[index]
    axes[1].plot(t_min, delay_base, label="DL Path Delay Baseline", color="#4C78A8")
    axes[1].plot(t_min, delay_worst, label="DL Path Delay Worst-Case", color="#E45756")
    axes[1].set_ylabel("Delay (ms)")
    axes[1].set_title("End-to-End Delay Proxy")
    axes[1].grid(True, alpha=0.25)
    axes[1].legend(loc="upper right")
    axes[1].set_xlabel("Time (min)")

    _save(fig, "03_e2e_bler_delay.png")


def make_interference_power(data: dict[str, object]) -> None:
    t_min = np.arange(data["n_steps"]) * data["sample_time_s"] / 60.0  # type: ignore[operator]
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    panels = [
        ("DL Worst-Case", "simDL_Worst"),
        ("UL Worst-Case", "simUL_Worst"),
    ]

    for ax, (title, key) in zip(axes, panels):
        sim = data["sims"][key]  # type: ignore[index]
        ax.plot(t_min, _dbm(sim["PS_mW"]), label="Signal Power", color="#4C78A8")
        ax.plot(t_min, _dbm(sim["PI_mW"]), label="CCI Power", color="#F58518")
        ax.plot(t_min, _dbm(sim["PJ_mW"]), label="Jammer Power", color="#E45756")
        ax.plot(t_min, sim["Prx_dBm"], label="Received Power", color="#54A24B", linewidth=1.1)
        ax.set_ylabel("Power (dBm)")
        ax.set_title(title)
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("Time (min)")
    _save(fig, "04_interference_power_worstcase.png")


def write_outputs(data: dict[str, object], summary_text: str) -> None:
    metrics = {
        "stage_label": "V7.0 Engineering Delivery",
        "project_name": data["project_name"],
        "startup_mode": data["startup_mode"],
        "worst_target": data["worst_target"],
        "sample_time_s": data["sample_time_s"],
        "orbit_minutes": round(float(data["orbit_minutes"]), 2),
        "constellation": {
            "num_planes": data["num_planes"],
            "sats_per_plane": data["sats_per_plane"],
            "total_sats": int(data["num_planes"]) * int(data["sats_per_plane"]),
        },
        "num_jammers": data["num_jammers"],
        "worst_case_enabled": data["worst_case_enabled"],
        "classifier_enabled": data["classifier_enabled"],
        "jam_scale_best_db": round(float(data["jam_scale_best_db"]), 3),
        "jam_info_code": [round(float(x), 6) for x in data["jam_info_code"]],
        "performance": {
            "dl_base_mean_thr_mbps": round(float(data["sims"]["simDL_Base"]["meanThr"]), 2),  # type: ignore[index]
            "dl_worst_mean_thr_mbps": round(float(data["sims"]["simDL_Worst"]["meanThr"]), 2),  # type: ignore[index]
            "dl_worst_outage_pct": round(_pct(data["sims"]["simDL_Worst"]["outageFrac"]), 2),  # type: ignore[index]
            "ul_base_mean_thr_mbps": round(float(data["sims"]["simUL_Base"]["meanThr"]), 2),  # type: ignore[index]
            "ul_worst_mean_thr_mbps": round(float(data["sims"]["simUL_Worst"]["meanThr"]), 2),  # type: ignore[index]
            "ul_worst_outage_pct": round(_pct(data["sims"]["simUL_Worst"]["outageFrac"]), 2),  # type: ignore[index]
            "e2e_base_mean_thr_mbps": round(float(data["sims"]["simE2E_Base"]["meanThr"]), 2),  # type: ignore[index]
            "e2e_worst_mean_thr_mbps": round(float(data["sims"]["simE2E_Worst"]["meanThr"]), 2),  # type: ignore[index]
            "e2e_worst_outage_pct": round(_pct(data["sims"]["simE2E_Worst"]["outageFrac"]), 2),  # type: ignore[index]
        },
        "source_result_mat": str(RESULT_PATH),
        "source_summary_txt": str(SUMMARY_PATH),
        "analysis_note": "Fresh MATLAB rerun was not performed because the matlab executable was not found on this machine during analysis.",
    }

    (THIS_DIR / "metrics_snapshot.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    shutil.copy2(SUMMARY_PATH, THIS_DIR / "source_summary_v7.txt")

    summary_lines = summary_text.splitlines()
    generated_line = next((line for line in summary_lines if line.startswith("Generated:")), "Generated: unknown")

    readme = f"""# V7工程状态分析

## 结论

- 当前工程已经进化到 **V7.0 Engineering Delivery / 工程交付版**。
- 主链路已经不是早期单下行脚本，而是 `DL + UL + E2E` 一体化工程版本。
- 最劣搜索链路 `InfoGAN + GA` 已接入，目标默认为 `{data["worst_target"]}`。
- 干扰识别链 `STFT + LeNet` 已接入，并在配置中处于启用状态。
- Dashboard、参数配置页、3D Viewer、合规表/合规灯都已经进入工程化形态。

## 这一步意味着什么

- 已经具备“交付版工程”骨架，而不是单一算法 demo。
- 已经能用统一配置同时评估下行、上行和端到端吞吐/中断。
- 已经有最劣工况搜索与分类识别能力，可支撑论文和平台展示。
- 但还没有完全走到“实测数据闭环”终态。
  - `README_使用说明.txt` 明确写了：上行链路中的 CCI 与 Jammer 仍是工程代理模型。
  - 换算后信号强度检查默认关闭，仍等待天线因子、线损、前放增益等真实接口参数。

## 本次分析来源

- 源结果：`{RESULT_PATH}`
- 源摘要：`{SUMMARY_PATH}`
- 历史运行：`{generated_line}`
- 本机状态：2026-03-25 检查时未找到 `matlab` 可执行文件，因此**没有做新的 MATLAB 复跑**；下面的图来自现有 V7 结果包重新整理。

## 当前运行快照

- 项目名：`{data["project_name"]}`
- 启动模式：`{data["startup_mode"]}`
- 采样间隔：`{data["sample_time_s"]} s`
- 轨道覆盖时长：约 `{float(data["orbit_minutes"]):.2f} min`
- 星座规模：`{data["num_planes"]} x {data["sats_per_plane"]} = {int(data["num_planes"]) * int(data["sats_per_plane"])}`
- 干扰星数量：`{data["num_jammers"]}`
- 最劣搜索：`{data["worst_case_enabled"]}`
- 分类识别：`{data["classifier_enabled"]}`
- 最优干扰放大量：`{float(data["jam_scale_best_db"]):.3f} dB`
- 最优 InfoCode：`{[round(float(x), 4) for x in data["jam_info_code"]]}`

## 关键性能

| 指标 | Baseline | Worst-Case |
| --- | ---: | ---: |
| DL Mean Throughput (Mbps) | {float(data["sims"]["simDL_Base"]["meanThr"]):.2f} | {float(data["sims"]["simDL_Worst"]["meanThr"]):.2f} |
| DL Outage (%) | {100 * float(data["sims"]["simDL_Base"]["outageFrac"]):.2f} | {100 * float(data["sims"]["simDL_Worst"]["outageFrac"]):.2f} |
| UL Mean Throughput (Mbps) | {float(data["sims"]["simUL_Base"]["meanThr"]):.2f} | {float(data["sims"]["simUL_Worst"]["meanThr"]):.2f} |
| UL Outage (%) | {100 * float(data["sims"]["simUL_Base"]["outageFrac"]):.2f} | {100 * float(data["sims"]["simUL_Worst"]["outageFrac"]):.2f} |
| E2E Mean Throughput (Mbps) | {float(data["sims"]["simE2E_Base"]["meanThr"]):.2f} | {float(data["sims"]["simE2E_Worst"]["meanThr"]):.2f} |
| E2E Outage (%) | {100 * float(data["sims"]["simE2E_Base"]["outageFrac"]):.2f} | {100 * float(data["sims"]["simE2E_Worst"]["outageFrac"]):.2f} |

## 已生成图

- `plots/00_stage_overview.png`
- `plots/01_throughput_timeseries.png`
- `plots/02_sinr_timeseries.png`
- `plots/03_e2e_bler_delay.png`
- `plots/04_interference_power_worstcase.png`

## 附件

- `metrics_snapshot.json`
- `source_summary_v7.txt`
"""

    (THIS_DIR / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"

    data, summary_text = load_result()
    make_stage_overview(data)
    make_throughput_timeseries(data)
    make_sinr_timeseries(data)
    make_e2e_quality(data)
    make_interference_power(data)
    write_outputs(data, summary_text)


if __name__ == "__main__":
    main()
