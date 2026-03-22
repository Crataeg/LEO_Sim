# SCI论文写作大纲：低轨卫星通信 EMC 仿真平台

## 0. 生成说明

- 本大纲聚焦“我们的卫星仿真平台”本身，优先突出平台架构、系统级建模、最劣干扰搜索、EMC 评估与工程可复现性。
- 当前会话环境未检测到 `matlab.exe`，因此本次图片不是现场重跑 MATLAB 生成，而是基于工程内已归档的 `outputs_v7/result_v7.mat`、`summary_v7.txt` 和 `dataset_stft_r2021a/_exports` 重新整理生成。
- 若后续补齐 MATLAB R2021a 及相关工具箱，可直接在工程目录执行 `run_V7_default.m` 或 `LEO_StarNet_EMC_V7_0_Engineering.m` 复现主结果。

## 1. 论文定位

- 论文类型建议定位为“平台/框架型研究论文”，不是单一算法论文。
- 核心卖点应放在：`LEO 场景建模 + DL/UL/E2E 联合链路仿真 + EMC 约束评估 + InfoGAN+GA 最劣工况搜索 + STFT/LeNet 干扰识别辅助链路` 的一体化平台。
- 写作时建议把 `InfoGAN` 和 `STFT+LeNet` 定义为平台增强模块，不要把它们写成唯一主创新点。
- 主文建议强调“工程可交付、可配置、可输出合规性结果、可复用到车载终端场景”。

## 2. 备选题目

### 中文题目

1. 面向车载低轨卫星通信系统的 EMC 仿真平台构建与最劣干扰评估
2. 一种集成最劣场景搜索与干扰识别的低轨卫星通信 EMC 仿真平台
3. 车载低轨卫星通信系统端到端 EMC 仿真平台及其最劣工况分析

### 英文题目

1. An EMC-Oriented Simulation Platform for Vehicle-Mounted LEO Satellite Communications with Worst-Case Interference Search
2. An Integrated LEO Satellite Communication EMC Simulation Framework with Joint Link Evaluation, Worst-Case Search, and Interference Identification
3. End-to-End EMC Simulation Platform for Vehicle-Mounted LEO Satellite Systems under Adversarial Interference Conditions

## 3. 摘要写法骨架

### 第一段：问题背景

- 低轨卫星通信在车载广域覆盖、空天地一体化网络和复杂电磁环境测试方面需求快速增长。
- 现有研究往往分别讨论链路性能、频谱共存、抗干扰算法或识别算法，缺少面向工程交付的一体化 EMC 仿真平台。

### 第二段：本文做了什么

- 构建了一个面向车载 LEO 通信系统的系统级 EMC 仿真平台。
- 平台集成 `satelliteScenario` 场景建模、DL/UL 双链路功率预计算、端到端路由求解、最劣干扰搜索、STFT 图像化识别以及合规性输出。

### 第三段：方法与结果

- 以 `1200 km / 53° / 12×8` LEO 星座和 `6` 个 jammer 为例，在 `10 s` 采样间隔下完成一个轨道周期仿真，总时长约 `109.33 min`。
- 基线工况下，E2E 平均吞吐量为 `73.99 Mbps`，中断率为 `0%`。
- 最劣工况下，E2E 平均吞吐量下降至 `50.57 Mbps`，相对下降 `31.66%`，中断率升至 `21.65%`；其中上行链路对干扰更敏感，最劣工况中断率达到 `20.73%`，显著高于下行链路的 `4.42%`。

### 第四段：结论与意义

- 结果表明该平台能够在统一框架内刻画 LEO 场景、EMC 约束与干扰风险传播过程。
- 该平台适合用于方案论证、参数扫描、最劣场景预评估及后续实验室验证支撑。

## 4. 正文大纲

## 4.1 Introduction

- 第 1 段：写 LEO 星座和车载终端场景的重要性，引出空天地融合、动态链路和电磁兼容问题。
- 第 2 段：写传统方法不足。现有工作要么偏物理层链路，要么偏单独 EMC 评估，要么偏识别/抗干扰算法，缺少统一平台。
- 第 3 段：写研究空白。缺少同时覆盖 `场景构建-功率求解-最劣搜索-识别辅助-合规性输出` 的工程型仿真框架。
- 第 4 段：列出本文贡献，建议压缩成 4 点。

### 建议贡献表述

1. 提出一个面向车载 LEO 通信系统的系统级 EMC 仿真平台，实现 DL/UL/E2E 联合评估。
2. 将 `InfoGAN + GA` 引入最劣干扰场景搜索，实现从参数扫描到数据驱动最差工况生成的统一流程。
3. 将 `STFT + LeNet` 作为识别支链接入平台输出，实现仿真时序到干扰图像和类别判别的联动。
4. 形成可直接落地的结果、摘要与合规性输出，为实验室测试与工程方案迭代提供依据。

## 4.2 Related Work

### 4.2.1 LEO/NGSO 场景与系统级仿真

- 重点引用：
- `01_A_Survey_on_Non_Geostationary_Satellite_Systems_The_Communication_Perspective.pdf`
- `02_LEO_Satellite_Access_Network_Towards_6G_The_Road_to_Space_Coverage.pdf`
- `LEO_Satellite_Communication_Simulation_Framework_for_Connected_Vehicles.pdf`
- 这一节说明本文不是重新发明单个链路模型，而是在车载场景下做工程平台整合。

### 4.2.2 干扰共存与 EMC 评估

- 重点引用：
- `03_Emerging_NGSO_Constellations_Spectral_Coexistence_with_GSO_Systems.pdf`
- `04_Evaluating_S_Band_Interference_Impact_of_Satellite_Systems_on_Terrestrial_Networks.pdf`
- `05_Null_Shaping_for_Interference_Mitigation_in_LEO_Satellites.pdf`
- `试验室环境下低轨卫星通信系统EMC仿真技术.docx`
- 这一节需要说明本文平台如何把频谱共存、CCI、jammer 和 EMC 指标合并到同一个结果链路。

### 4.2.3 最劣搜索与干扰识别

- 重点引用：
- `06_InfoGAN_Interpretable_Representation_Learning_by_Information_Maximizing_GANs.pdf`
- `07_Gradient_Based_Learning_Applied_to_Document_Recognition_LeNet.pdf`
- `08_Hierarchical_Classification_Method_for_RFI_Recognition_and_Characterization_in_Satcom.pdf`
- `09_RF_Based_Low_SNR_Classification_of_UAVs_Using_CNNs.pdf`
- `10_Modulation_Classification_Through_Deep_Learning_Using_Resolution_Transformed_Spectrograms.pdf`
- 这一节必须收住表述：依据知识库审查结论，`InfoGAN` 和 `STFT+LeNet` 在当前知识库中更适合作为“平台增强模块”和“工程实现支链”，不建议写成最核心学术创新。

## 4.3 Platform Architecture and System Model

### 4.3.1 平台总架构

- 用 [01_platform_architecture.png](./01_platform_architecture.png)。
- 对应代码主入口：
- `v7proj/LEO_StarNet_EMC_V7_0_Engineering.m`
- `emcDefaultConfig.m`
- `emcBuildLinkModel.m`
- `simulateStarNetV7.m`
- `emcComputeComplianceRowsV7.m`

### 4.3.2 场景与几何建模

- 写清场景参数：
- 轨道高度 `1200 km`
- 轨道倾角 `53°`
- 星座规模 `12 × 8 = 96 satellites`
- 频率复用因子 `ReuseK = 4`
- jammer 数量 `6`
- 用户站：`(36.06, 120.38)`
- 网关站：`(39.90, 116.40)`
- 采样间隔 `10 s`
- 仿真时长 `1 orbital period ≈ 109.33 min`

### 4.3.3 链路与 EMC 模型

- 下行：`Fc = 1.5 GHz, BW = 20 MHz`
- 上行：`Fc = 1.6 GHz, BW = 20 MHz`
- 需要在正文中给出 4 组核心公式：
- 自由空间路径损耗和接收功率公式
- CCI 与 jammer 聚合功率公式
- `SINR -> BER -> THR` 指标代理公式
- `E2E throughput = min(DL, UL)` 与端到端时延估计公式

### 4.3.4 EMC 约束与合规性指标

- 写清平台判据：
- `Min SINR = 1 dB`
- `Min Throughput = 20 Mbps`
- `Rx Sensitivity = -120 dBm`
- `Max Doppler Rate = 300 Hz/s`
- Ku 链路相关 EIRP、G/T 和 JA3700 等项目约束
- 这里要强调平台不是“单纯通信仿真”，而是“通信性能 + EMC 门限 + 工程输出”的联合框架。

## 4.4 Worst-Case Search and Interference Identification Modules

### 4.4.1 InfoGAN + GA 最劣工况搜索

- 说明平台中 `InfoGAN` 先学习 jammer 包络，再由 `GA` 在 `z + c + JamScale` 空间搜索最差解。
- 关键参数：
- `GAN_seqLen = 128`
- `GAN_zDim = 16`
- `GAN_cDim = 2`
- `GAN_trainIters = 250`
- `GA_PopSize = 16`
- `GA_Generations = 10`
- 最优干扰放大因子：`JamScaleBest_dB = 26.74 dB`

### 4.4.2 STFT + LeNet 干扰识别支链

- 说明这部分是从功率级时序映射到 IQ 快照和 STFT 图像，再由 `LeNet` 分类。
- 类别可写成 `none / tone / pbnj / mod`。
- 用图：
- [stft_confusion_test.png](./stft_confusion_test.png)
- [stft_keyframes_montage.png](./stft_keyframes_montage.png)
- [stft_train_montage.png](./stft_train_montage.png)

### 4.4.3 模块在平台中的角色

- 最好明确两句话：
- `InfoGAN + GA` 用于找到更具破坏性的输入条件。
- `STFT + LeNet` 用于解释平台在时间轴上遇到的干扰形态，不替代主链路求解器。

## 4.5 Experimental Settings

- 建议把这一节写成“可复现实验配置”。
- 表 1 放系统与场景参数。
- 表 2 放最劣搜索参数。
- 表 3 放 EMC 门限。
- 明确比较对象：
- `Baseline`
- `Worst-case`
- 三条评估链：
- `Downlink`
- `Uplink`
- `End-to-End`

## 4.6 Results and Analysis

### 4.6.1 平台整体统计结果

- 用 [02_link_summary_bars.png](./02_link_summary_bars.png)。
- 建议正文直接写实数，不要只写“明显下降”。

### 建议写入的关键数据

- DL 基线平均吞吐量：`78.97 Mbps`
- DL 最劣平均吞吐量：`75.97 Mbps`
- DL 最劣中断率：`4.42%`
- UL 基线平均吞吐量：`75.69 Mbps`
- UL 最劣平均吞吐量：`52.62 Mbps`
- UL 最劣中断率：`20.73%`
- E2E 基线平均吞吐量：`73.99 Mbps`
- E2E 最劣平均吞吐量：`50.57 Mbps`
- E2E 最劣中断率：`21.65%`

### 可直接写成结论句

- 最劣搜索导致 E2E 平均吞吐量下降 `31.66%`。
- 上行链路比下行链路更脆弱，说明卫星接收侧在最劣 jammer 场景下更容易成为系统瓶颈。

### 4.6.2 时间动态过程分析

- 用 [03_throughput_timeseries.png](./03_throughput_timeseries.png)。
- 重点写：
- 最劣包络不是全程都致命，但会形成集中失效窗口。
- E2E 失效主要继承自 UL 降级，这与 `min(DL, UL)` 的端到端定义一致。

### 4.6.3 功率分解与干扰机理

- 用 [04_power_breakdown_worst.png](./04_power_breakdown_worst.png)。
- 这一节解释 `Signal / CCI / Jammer / Noise` 的相对变化。
- 关键落点：
- jammer 在若干时段抬升到主导项，直接压低 SINR。
- 下行链路仍具一定冗余，而上行链路更容易被 jammer 与代理 CCI 联合拉低。

### 4.6.4 最劣包络与中断窗口

- 用 [05_jammer_outage_windows.png](./05_jammer_outage_windows.png)。
- 可写数字：
- jammer 包络均值约 `0.375`
- jammer 包络最大值约 `0.893`
- `jamAgg > 0.5` 的时间占比约 `30.79%`
- E2E 最劣工况中断总时长约 `23.67 min`
- UL 最劣工况中断总时长约 `22.67 min`
- DL 最劣工况中断总时长约 `4.83 min`

### 4.6.5 干扰识别可视化分析

- 这里不要过度承诺“识别精度领先”。
- 更稳妥的写法是：
- 平台不仅输出链路指标，还能导出干扰时频图和混淆矩阵，用于辅助解释平台在关键时刻所处的干扰类别。
- 该支链增强了平台的可解释性和工程诊断能力。

## 4.7 Discussion

### 4.7.1 平台优势

- 支持 `DL/UL/E2E` 联合评估，而不是单链路孤立分析。
- 将 EMC 指标、链路性能、最劣搜索与识别输出统一到一个结果文件链路中。
- 具备较强的工程可配置性和交付属性。

### 4.7.2 局限性

- 当前平台是“系统级功率仿真 + 指标代理模型”，不是全波形细粒度物理层仿真。
- `InfoGAN` 与 `STFT+LeNet` 的文献支撑在知识库中仍偏弱，写作中应避免过度拔高。
- 目前结果来自归档工程输出，后续最好在真实 MATLAB 环境中增加重复试验、参数敏感性分析和消融实验。

### 4.7.3 后续工作

- 增加多终端、多业务和多网关切换场景。
- 增加参数敏感性与统计置信区间。
- 将实测数据或实验室注入干扰数据回灌到平台。
- 强化生成式干扰建模和识别模块的正式文献支撑。

## 4.8 Conclusion

- 结论建议分三句写：
- 第一句总结平台构建完成了什么。
- 第二句总结最劣工况下的核心量化退化结果。
- 第三句总结平台对工程评估、EMC 验证和后续测试方案设计的意义。

## 5. 图表安排建议

## 图

- 图 1：平台总体架构图，对应 [01_platform_architecture.png](./01_platform_architecture.png)
- 图 2：基线与最劣工况下的吞吐量/中断率汇总，对应 [02_link_summary_bars.png](./02_link_summary_bars.png)
- 图 3：DL/UL/E2E 吞吐量时间序列与 jammer 包络，对应 [03_throughput_timeseries.png](./03_throughput_timeseries.png)
- 图 4：最劣工况功率分解图，对应 [04_power_breakdown_worst.png](./04_power_breakdown_worst.png)
- 图 5：最劣 jammer 包络与中断窗口，对应 [05_jammer_outage_windows.png](./05_jammer_outage_windows.png)
- 图 6：测试集混淆矩阵，对应 [stft_confusion_test.png](./stft_confusion_test.png)
- 图 7：关键时刻 STFT 拼图，对应 [stft_keyframes_montage.png](./stft_keyframes_montage.png)

## 表

- 表 1：系统场景与链路参数表
- 表 2：最劣搜索与 anti-jam 参数表
- 表 3：EMC 与合规性判据表
- 表 4：DL/UL/E2E 基线与最劣工况性能汇总表
- 表 5：平台模块与代码映射表

## 6. 推荐写作策略

- 如果目标是较稳的 SCI 投稿，主创新建议写成“面向车载 LEO 通信的统一 EMC 仿真平台”。
- `InfoGAN` 与 `STFT+LeNet` 放在增强模块或案例模块中，更容易自洽。
- 正文应把“平台集成度、工程可复现性、统一输出链路、EMC 约束嵌入”作为第一主线。
- 若要冲更强的期刊，需要追加：
- 多随机种子重复实验
- 更多场景对比
- 消融实验
- 真实测量数据或硬件在环验证

## 7. 大纲所依据的关键资产

- `obsidian知识库/00_项目总览.md`
- `obsidian知识库/40_代码级技术解析/卫星仿真平台_代码级技术解析.md`
- `成果本身/代码工程/LEO_Sim/README.md`
- `成果本身/代码工程/LEO_Sim/卫星仿真平台子知识库/01_平台架构/卫星仿真平台技术栈.md`
- `成果本身/代码工程/LEO_Sim/卫星仿真平台子知识库/02_代码映射/平台代码-论文映射.md`
- `obsidian知识库/30_写作基础/技术涉及文献与报告总结.md`
- `成果本身/代码工程/LEO_Sim/LEO_Sim/LEO_Sim_V7/v7proj/outputs_v7/result_v7.mat`
- `成果本身/代码工程/LEO_Sim/LEO_Sim/LEO_Sim_V7/v7proj/outputs_v7/summary_v7.txt`
- `成果本身/代码工程/LEO_Sim/LEO_Sim/LEO_Sim_V7/v7proj/dataset_stft_r2021a/_exports/`

## 8. 本次已生成的交付物

- [SCI论文写作大纲_卫星仿真平台.md](./SCI论文写作大纲_卫星仿真平台.md)
- [paper_metrics_summary.csv](./paper_metrics_summary.csv)
- [summary_v7.txt](./summary_v7.txt)
- [01_platform_architecture.png](./01_platform_architecture.png)
- [02_link_summary_bars.png](./02_link_summary_bars.png)
- [03_throughput_timeseries.png](./03_throughput_timeseries.png)
- [04_power_breakdown_worst.png](./04_power_breakdown_worst.png)
- [05_jammer_outage_windows.png](./05_jammer_outage_windows.png)
- [stft_confusion_test.png](./stft_confusion_test.png)
- [stft_keyframes_montage.png](./stft_keyframes_montage.png)
- [stft_train_montage.png](./stft_train_montage.png)
- [generate_platform_paper_assets.py](./generate_platform_paper_assets.py)
