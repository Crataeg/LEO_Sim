# IEICE进化目录总览

创建日期：`2026-03-24`

## 目录目的

这个目录用于把现有卫星仿真平台从“项目工程/平台演示”进化到更适合 `IEICE Transactions on Communications` 的论文工作面。

## 当前包含内容

### 1. 基线快照

- `baseline_snapshot/LEO_Sim`
- `baseline_snapshot/试验室环境下低轨卫星通信系统EMC仿真技术`

说明：
- 这里是当前成果的冻结副本，后续进化尽量在本目录下开展，不直接污染旧成果。

### 2. 脚本

- `scripts/generate_platform_paper_assets.py`
- `scripts/download_constellation_data.py`
- `scripts/plot_constellation_overview.py`

说明：
- `generate_platform_paper_assets.py` 是之前用于从已有 `result_v7.mat` 二次整理论文图的脚本。
- `download_constellation_data.py` 用于下载开源星座数据。
- `plot_constellation_overview.py` 用于生成初步的壳层分布图。

### 3. 研究笔记

- `research_notes/IEICE方向初步反思.md`
- `research_notes/之前图表脚本说明.md`
- `research_notes/constellation_data_integration_note.md`
- `research_notes/figures/constellation_shell_overview.png`
- `research_notes/figures/constellation_shell_summary.csv`

### 4. 下载材料

- `downloads/constellation_data`
- `downloads/papers/Transactions_on_Communications_satellite`
- `downloads/papers/Transactions_on_Communications_format_template`

说明：
- `constellation_data` 是从 CelesTrak 官方接口下载的当前星座数据。
- `papers` 下保留了 IEICE 论文与格式模板，方便在同一工作面内使用。

## 当前初步结论

- 当前工程直接投 IEICE 仍偏工程化、偏仿真展示。
- 引入开源星座数据是值得做的第一步。
- 下一阶段建议把论文主线收束为：
  - `真实公开星座数据驱动的 LEO 链路/EMC 评估`
  - 或
  - `真实星座约束下的最劣干扰场景分析`

## 下一步推荐

1. 基于 CelesTrak 数据增加青岛/北京上空可见卫星数时间序列。
2. 做 `Starlink / OneWeb / 自定义12x8` 三组场景对比。
3. 在工程中单独开一支“real-constellation branch”，不要一上来改主工程。
4. 收缩论文贡献，弱化 Dashboard 和杂项导出，强化数据锚定和机理分析。
