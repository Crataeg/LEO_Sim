# 本轮 MATLAB 运行结论

日期：`2026-03-27`

## 1. 运行环境

- MATLAB 版本：`R2021a`
- 已安装：
  - `Communications Toolbox`
  - `Satellite Communications Toolbox`
  - `Deep Learning Toolbox`
  - `Image Processing Toolbox`
  - `Signal Processing Toolbox`
  - `Simulink`
  - 以及若干其他工具箱

## 2. 当前工具箱状态

当前关键工具箱均已到位，包括：
- `Satellite Communications Toolbox`
- `Communications Toolbox`
- `Deep Learning Toolbox`
- `Image Processing Toolbox`
- `Optimization Toolbox`
- `Global Optimization Toolbox`

证据：
- `11_运行环境与依赖/matlab_toolboxes_20260327.txt`
- `11_运行环境与依赖/function_availability_20260327.txt`
- 其中：
  - `ga => 2`

## 3. 完整工程运行状态

### 直接按完整主链运行

使用配置：
- `cfg.Output.Enable3DViewer = false`

结果：
- 主链仿真成功
- `InfoGAN + GA` 最劣搜索成功
- STFT 数据集与 LeNet 训练成功
- confusion matrix 成功导出
- keyframes 成功导出

补充说明：
- 最后出现的 `timer / device or resource busy` 提示发生在 Viewer/Dashboard 收尾阶段
- 不影响结果文件和导出图生成

## 4. 当前最重要的产物

### 主结果

- `outputs_v7/cfg_resolved_v7.mat`
- `outputs_v7/result_v7.mat`
- `outputs_v7/summary_v7.txt`

### 识别支链图

- `dataset_stft_r2021a_exports/confusion_test.png`
- `dataset_stft_r2021a_exports/montage_train.png`
- `dataset_stft_r2021a_exports/sim_keyframes_montage.png`

## 5. 当前能写进论文的结论

当前可以写：
- MATLAB 环境恢复正常
- 系统级平台主链可运行
- 完整 `InfoGAN + GA` 最劣搜索已运行
- 识别支链结果可导出

当前仍需注意：
- Dashboard / 3D Viewer 在非交互环境下可能出现资源占用提示

## 6. 最后的判断

当前工程已经恢复到了：
- `主框架可跑`
- `识别支链可训`
- `最劣搜索缺一个工具箱`

所以从论文推进角度看，当前最现实的状态是：

`系统级平台论文已经有足够结果可写，而且主链、最劣搜索和识别支链都已经形成完整可引用结果。`
