# V7工程状态分析

## 结论

- 当前工程已经进化到 **V7.0 Engineering Delivery / 工程交付版**。
- 主链路已经不是早期单下行脚本，而是 `DL + UL + E2E` 一体化工程版本。
- 最劣搜索链路 `InfoGAN + GA` 已接入，目标默认为 `e2e`。
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

- 源结果：`D:\论文卫星\LEO_Sim\产出文件夹\卫星仿真平台工程文件夹_最终版\LEO_Sim\LEO_Sim\LEO_Sim_V7\v7proj\outputs_v7\result_v7.mat`
- 源摘要：`D:\论文卫星\LEO_Sim\产出文件夹\卫星仿真平台工程文件夹_最终版\LEO_Sim\LEO_Sim\LEO_Sim_V7\v7proj\outputs_v7\summary_v7.txt`
- 历史运行：`Generated: 09-Mar-2026 21:01:47`
- 本机状态：2026-03-25 检查时未找到 `matlab` 可执行文件，因此**没有做新的 MATLAB 复跑**；下面的图来自现有 V7 结果包重新整理。

## 当前运行快照

- 项目名：`车载低轨卫星通信系统EMC性能正向设计技术研究 | V7.0`
- 启动模式：`default`
- 采样间隔：`10.0 s`
- 轨道覆盖时长：约 `109.17 min`
- 星座规模：`12 x 8 = 96`
- 干扰星数量：`6`
- 最劣搜索：`True`
- 分类识别：`True`
- 最优干扰放大量：`26.741 dB`
- 最优 InfoCode：`[0.0574, 0.0174]`

## 关键性能

| 指标 | Baseline | Worst-Case |
| --- | ---: | ---: |
| DL Mean Throughput (Mbps) | 78.97 | 75.97 |
| DL Outage (%) | 0.00 | 4.42 |
| UL Mean Throughput (Mbps) | 75.69 | 52.62 |
| UL Outage (%) | 0.00 | 20.73 |
| E2E Mean Throughput (Mbps) | 73.99 | 50.57 |
| E2E Outage (%) | 0.00 | 21.65 |

## 已生成图

- `plots/00_stage_overview.png`
- `plots/01_throughput_timeseries.png`
- `plots/02_sinr_timeseries.png`
- `plots/03_e2e_bler_delay.png`
- `plots/04_interference_power_worstcase.png`

## 附件

- `metrics_snapshot.json`
- `source_summary_v7.txt`
