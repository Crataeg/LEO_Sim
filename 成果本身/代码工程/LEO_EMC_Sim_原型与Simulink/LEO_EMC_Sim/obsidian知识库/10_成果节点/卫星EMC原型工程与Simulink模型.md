---
title: "卫星EMC原型工程与Simulink模型"
task_type: "成果"
source_path: "D:\一汽项目"
copied_path: "D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink"
---
# 卫星EMC原型工程与Simulink模型

## 节点总结

该节点保留一汽项目中的 Simulink 原型工程、根目录系统模型和构建缓存，是论文卫星线分析平台演进过程的重要工程补充。

## 写作价值

适合在论文中说明平台从原型到工程化版本的演进路线与验证链。

## 原始位置

- `D:\一汽项目`

## 来源条目

- `LEO_EMC_Sim`
- `build_LEO_EMC_Sim.m`
- `LEO_EMC_System.slx`
- `LEO_EMC_System.slx.autosave`
- `LEO_EMC_System.slxc`
- `slprj`

## 复制后位置

- `D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink`

## 文件规模

- 文件数：`142`

## 关键文件

- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\build_LEO_EMC_Sim.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\build_LEO_EMC_Sim.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\cfo_comp.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\interf_gen.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\LEO_Sim_V1.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\preamble_insert.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\run_LEO_EMC_Sim.m`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\LEO_EMC_Sim_说明报告.docx`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\LEO_EMC_仿真技术_主流方法与文献支撑_说明报告.docx`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\.vscode\settings.json`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\.vscode\tasks.json`
- `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_System.slx`

## 代表性内容预览

### `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\build_LEO_EMC_Sim.m`

```text
function build_LEO_EMC_Sim()
% LEO EMC 通信视角 Simulink 自动建模脚本（Comm Toolbox + Stateflow 写 Script）
% R2021a兼容：MATLAB Function block 在Simulink层面可能表现为SubSystem；需通过 Stateflow.EMChart.Script 写入代码

assert(license('test','communication_toolbox')==1, "Communications Toolbox 未授权");
assert(license('test','stateflow')==1, "Stateflow 未授权（MATLAB Function block 需要）");

model = 'LEO_EMC_Sim_Simulink';
if bdIsLoaded(model); close_system(model,0); end
if exist([model '.slx'],'file'); delete([model '.slx']); end

new_system(model);
open_system(model);

cfg = defaultCfg();
assignin('base','cfg',cfg);

set_param(model,'Solver','FixedStepDiscrete');
set_param(model,'FixedStep', num2str(cfg.sim.Ts));
set_param(model,'StopTime',  cfg.sim.StopTime);

% 顶层子系统
add_block('built-in/Subsystem',[model '/TX'],          'Position',[80 80 260 260]);
add_block('built-in/Subsystem',[model '/Channel_EMC'], 'Position',[320 80 540 260]);
add_block('built-in/Subsystem',[model '/RX'],          'Position',[600 80 820 260]);
add_block('built-in/Subsystem',[model '/Metrics'],     'Position',[880 80 1120 260]);

buildTX([model '/TX']);
buildChannelEMC([model '/Channel_EMC']);
buildRX([model '/RX']);
buildMetrics([model '/Metrics']);

set_param(model,'SimulationCommand','update');

% 顶层连线
add_line(model,'TX/1','Channel_EMC/1','autorouting','on');
add_line(model,'Channel_EMC/1','RX/1','autorouting','on');
add_line(model,'RX/1
```

### `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\build_LEO_EMC_Sim.m`

```text
function build_LEO_EMC_Sim()
% build_LEO_EMC_Sim
% 一键生成 Simulink 模型：LEO卫星通信 EMC（通信视角）仿真骨架
%
% 依赖（推荐）：
%  - Simulink
%  - Communications Toolbox（用于QPSK调制/解调、卷积码/Viterbi、误码统计等模块）
%
% 生成：
%  - LEO_EMC_Sim_Simulink.slx

model = 'LEO_EMC_Sim_Simulink';
if bdIsLoaded(model); close_system(model,0); end
if exist([model '.slx'],'file'); delete([model '.slx']); end

new_system(model);
open_system(model);

% ---------- 全局参数（写入 Base Workspace，方便外行只改这里） ----------
cfg = defaultCfg();
assignin('base','cfg',cfg);

% ---------- 画布基础设置 ----------
set_param(model,'StopTime','cfg.sim.StopTime');
set_param(model,'Solver','FixedStepDiscrete');
set_param(model,'FixedStep','cfg.sim.Ts');

% ---------- 添加子系统：TX / Channel+EMC / RX / Metrics ----------
add_block('built-in/Subsystem',[model '/TX'], 'Position',[80 80 240 240]);
add_block('built-in/Subsystem',[model '/Channel_EMC'], 'Position',[320 80 520 240]);
add_block('built-in/Subsystem',[model '/RX'], 'Position',[600 80 760 240]);
add_block('built-in/Subsystem',[model '/Metrics'], 'Position',[840 80 1020 240]);

% 顶层连接：TX -> Channel_EMC -> RX -> Metrics

% ---------- 构建 TX ----------
buildTX([model '/TX']);

% ---------- 构建 Channel + EMC ----------
buildChannelEMC([model '/Channel_EMC']);

% ---------- 构建 RX ----------
buildRX([model '/RX']);

% ---------- 构建 Metrics ----------
buildMetrics([model '/Metrics']);
add_line(model,'TX/1','Channel_EMC/1','
```

### `成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\cfo_comp.m`

```text
function y = cfo_comp(r)
cfg = evalin('base','cfg');

rx = r(:);
N = length(rx);
Rs = cfg.phy.Rs;
t = (0:N-1).';

if cfg.rx.cfoMethod == 1
    cfo_hat = cfg.leo.fD_Hz;
else
    L = cfg.phy.preambleHalfLen;
    if N < 2*L
        cfo_hat = 0;
    else
        r1 = rx(1:L);
        r2 = rx(L+1:2*L);
        P = sum(conj(r1).*r2);
        cfo_hat = angle(P) * Rs / (2*pi*L);
    end
end

y = rx .* exp(-1j*2*pi*cfo_hat*t/Rs);
end

```

## 原文-工程行级对应与分析

### 1. “自动搭建 Simulink 通信链” -> 模型生成器
- 原文抓手：原型工程说明报告中“自动建模、R2021a 兼容、通信视角 Simulink”的表述。
- 工程对应：`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\build_LEO_EMC_Sim.m:1-20`；`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\build_LEO_EMC_Sim.m:74-205`
- 分析：`build_LEO_EMC_Sim()` 负责建模入口与时间步配置，`buildTX / buildChannelEMC / buildRX / buildMetrics` 把发射、信道干扰、接收和指标输出按块自动装配，所以该原型节点与报告文字是逐段对应的。

### 2. “干扰注入 + CFO 补偿” -> 关键接收机算法
- 原文抓手：说明文档和根目录简版材料里对同频噪声、单音、脉冲、邻频、同址耦合干扰，以及 CFO 估计/补偿的描述。
- 工程对应：`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\build_LEO_EMC_Sim.m:305-360`；`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\interf_gen.m:1-37`；`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\cfo_comp.m:1-23`
- 分析：`interf_gen` 负责五类等效干扰波形，`cfo_comp` 用前导相关估计并补偿频偏，这两条就是原型工程里“EMC 干扰 + 接收机恢复”的最小可运行闭环。

### 3. “物理层到链路评估” -> V1 原始仿真脚本
- 原文抓手：早期说明报告中对轨道、信道、干扰、蒙特卡罗误码和吞吐曲线的描述。
- 工程对应：`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\LEO_Sim_V1.m:123-178`；`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\LEO_Sim_V1.m:229-321`；`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\LEO_Sim_V1.m:585-634`
- 分析：`defaultConfig()` 固定场景、链路和干扰参数，`computeCNI()` 先算 `C/N/I/SINR`，`runMonteCarlo()` 与 `genInterferenceWaveform()` 再把这些功率量真正压成 BER/BLER/THR 结果，因此新增原型资产是 V7 工程化之前的底层证据链。

### 4. “参数可调的一键运行” -> 原型执行入口
- 原文抓手：说明报告中“修改 cfg 即可复现实验”的说法。
- 工程对应：`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\run_LEO_EMC_Sim.m:1-15`；`D:\论文卫星\成果本身\代码工程\LEO_EMC_Sim_原型与Simulink\LEO_EMC_Sim\preamble_insert.m:1-25`
- 分析：`run_LEO_EMC_Sim()` 只暴露 `cfg.emc.type / JS_dB / fD_Hz / cfoMethod` 等关键参数，`preamble_insert()` 负责帧结构组织，这说明原型工程的目标不是做复杂 UI，而是作为可快速复现实验的最小工程载体。
