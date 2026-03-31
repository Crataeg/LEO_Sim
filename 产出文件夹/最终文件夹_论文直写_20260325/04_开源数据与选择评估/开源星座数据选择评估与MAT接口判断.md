# 开源星座数据选择评估与 `.mat` 接口判断

## 1. 结论先行

### 1.1 当前下载的数据是不是最佳选择

结论：`如果目标是“最快进入工程、最快画出真实星座图”，当前选的 CelesTrak 是最佳第一选择。`

原因很直接：
- 公开可访问
- 机器可读
- 可直接按组下载
- 同时支持 `JSON / CSV / 2LE`
- 更新频率高
- 对 `Starlink / OneWeb / Qianfan` 已经有现成分组

### 1.2 但当前选择还不完整

如果只看我们最开始下的 `Starlink + OneWeb + Active`，还不够。

更适合当前论文方向的组合应该是：
- `Starlink`：国际主参照
- `Qianfan`：国内公开星座主参照
- `GeeSat/吉利`：国内车企相关补充参照

### 1.3 能不能直接从 `.mat` 输入接口喂进去

结论：`当前接口能接收 .mat 文件，但不能直接消费原始开源星座数据。`

更准确地说：
- `能加载 .mat`
- `不能直接把 TLE/JSON/CSV 里的真实卫星列表按现有逻辑跑起来`

当前接口只支持把 `.mat` 里的结构体并入 `cfg`，而 `cfg.Constellation` 现在仍是：
- 高度
- 倾角
- 轨道面数
- 每面卫星数
- 相位因子
- 复用因子

也就是：`它接收的是合成星座壳层参数，不是逐星轨道数据。`

## 2. 当前可选开源数据源对比

| 数据源 | 开放性 | 程序化访问 | 轨道精度/实时性 | 对 Starlink | 对国内星座 | 对车企相关星座 | 适合当前工程 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CelesTrak | 高 | 高 | 高 | 强 | 中到强 | 中 | 最优第一选择 |
| Space-Track | 中 | 高，但需账号 | 很强 | 强 | 强 | 强 | 如果后续追求权威性可升级 |
| UCS Satellite Database | 高 | 中 | 低于 GP/TLE | 弱 | 弱 | 弱 | 更适合元数据，不适合作图主源 |
| SatNOGS DB | 高 | 高 | 偏观测社区 | 中 | 中 | 中 | 适合补充，不适合替代轨道主源 |

### 当前判断

- `CelesTrak` 最适合作为当前工程第一阶段数据源。
- `Space-Track` 更权威，但门槛更高，不适合现在先手推进。
- `UCS / SatNOGS` 更适合补充元数据、运营方、平台类型，不适合直接替代轨道分布作图。

## 3. 具体对比：Starlink、Qianfan、GeeSat、OneWeb

## 3.1 Starlink

当前数据来源：
- `downloads/constellation_data/celestrak_starlink_gp.json`
- `downloads/constellation_data/celestrak_starlink_gp.2le`

当前统计：
- 数量：`9884`
- 平均轨道高度约：`483.7 km`
- 主要倾角簇：约 `43 deg / 53 deg / 70 deg / 97.x deg`

优点：
- 数据最完整
- 分组接口最成熟
- 适合做真实公开大星座对比

缺点：
- 与国内车企场景的叙事距离略远
- 如果只拿它做例子，论文容易偏“国际主流大星座案例”，不够本土化

## 3.2 Qianfan

当前数据来源：
- `downloads/constellation_data/celestrak_qianfan_gp.json`
- `downloads/constellation_data/celestrak_qianfan_gp.2le`

当前统计：
- 数量：`108`
- 平均轨道高度约：`1031.2 km`
- 当前倾角基本集中在：`89.0 deg`

优点：
- 国内公开星座
- 在 CelesTrak 里有独立分组
- 对“国内公开星座 vs Starlink”的对比非常方便

缺点：
- 相比 Starlink，当前规模仍小很多
- 生态、车端应用叙事不如车企自有星座直接

## 3.3 GeeSat / 吉利

当前数据来源不是独立分组，而是：
- 先下载 `downloads/constellation_data/celestrak_active_gp.csv`
- 再按对象名筛出 `GEESAT-*`
- 结果保存在 `downloads/constellation_data/celestrak_geesat_subset.csv`

当前统计：
- 数量：`63`
- 平均轨道高度约：`613.8 km`
- 倾角基本集中在：`50.0 deg`

优点：
- 与国内车企语境最贴近
- 对我们“车载低轨卫星通信”叙事最有针对性

缺点：
- CelesTrak 里没有现成 `GeeSat` 分组
- 自动化程度不如 `Starlink / OneWeb / Qianfan`
- 后续持续更新需要靠名字过滤，不如现成 group 稳

### 核心判断

如果你问“国内车企或者星链，谁更值得先接工程”：
- 从工程接入难度看：`Starlink > Qianfan > GeeSat`
- 从叙事贴合度看：`GeeSat > Qianfan > Starlink`
- 从折中角度看，当前最佳组合是：
  - `Starlink` 作为国际主参考
  - `Qianfan` 作为国内公开主参考
  - `GeeSat` 作为车企相关补充案例

## 3.4 OneWeb

当前统计：
- 数量：`651`
- 平均轨道高度约：`1198.1 km`
- 倾角主要在 `87.8~87.9 deg`

作用：
- 作为第二个国际参考组非常合适
- 但对当前“车企/星链重点对比”来说，优先级低于 `Qianfan` 和 `GeeSat`

## 4. 所以，我们当前数据选择要不要调整

结论：`要调整，但不是推翻。`

### 保留

- 保留 `Starlink`
- 保留 `OneWeb`
- 保留 `Active`

### 新增

- 新增 `Qianfan`
- 从 `Active` 中派生 `GeeSat`

### 推荐的数据优先级

1. `Starlink`
2. `Qianfan`
3. `GeeSat`
4. `OneWeb`
5. `Active` 作为总表兜底

## 5. 当前 `.mat` 输入接口到底能不能接

## 5.1 接口本身能读 `.mat`

当前入口在：
- `LEO_StarNet_EMC_V7_0_Engineering.m` 第 `857-899` 行

其中：
- 第 `871-887` 行会在输入是文件路径时执行 `load(arg1)`
- 第 `876-883` 行会寻找 `cfg` 结构体或任意结构体
- 然后通过 `emcMergeStruct.m` 第 `1-20` 行递归合并到默认配置

所以：
- `mat 文件输入` 这件事本身是支持的

## 5.2 但接口目前只认“壳层参数”，不认“逐星轨道数据”

问题在于：
- `emcDefaultConfig.m` 第 `22-31` 行定义的 `cfg.Constellation`
- 只有 `Altitude_m / Inclination_deg / NumPlanes / SatsPerPlane / FPhasing / ReuseK / ElMask_deg`

主程序在：
- `LEO_StarNet_EMC_V7_0_Engineering.m` 第 `58-67` 行
- 读取的也是这些标量壳层参数

后面真正建星座时：
- `LEO_StarNet_EMC_V7_0_Engineering.m` 第 `92-104` 行
- 用的是 `for p=1:numPlanes, for s=1:satsPerPlane` 的合成 Walker-like 星座生成方式

这意味着：
- 就算你把 `Starlink/Qianfan/GeeSat` 的原始 TLE/JSON 数据塞进 `.mat`
- 当前代码也不会直接用这些逐星轨道数据建星座

## 5.3 当前能做到的“半直接接入”

有两种层次：

### 方式 A：弱接入

把开源数据先压缩成：
- 平均高度
- 代表性倾角
- 轨道面数估计
- 每面卫星数估计

再写成 `.mat` 里的 `cfg.Constellation`

优点：
- 几乎不用改主代码

缺点：
- 只是“借用真实数据统计量”
- 不是真正加载真实星座

### 方式 B：强接入

扩展 `cfg` 结构，新增例如：
- `cfg.Constellation.Mode = 'synthetic' | 'external'`
- `cfg.Constellation.ExternalSatList`
- `cfg.Constellation.ExternalJammerList`

然后改主程序：
- 把 `92-104` 行的合成星座生成改成“若 external mode，则按逐星轨道元素建星”
- 把 `106-111` 行的 jammer 构造也改成可接外部对象

这是正确方向。

## 5.4 最终判断

所以问题的答案是：

- `开源卫星数据可以通过我们的 .mat 输入接口间接接入`
- `但目前不能原样直接接入`

如果不改代码：
- 只能把真实星座数据先做统计压缩，再写成 `cfg.Constellation`

如果想真正把 `Starlink / Qianfan / GeeSat` 当作真实星座输入：
- 必须扩展当前 `.mat` 配置格式
- 并修改主程序的星座生成逻辑

## 6. 最推荐的下一步

### 最优工程动作

1. 保留现有 `synthetic constellation` 主链不动。
2. 新开一个 `external-constellation branch`。
3. 先支持三类输入：
   - `Starlink`
   - `Qianfan`
   - `GeeSat`
4. 输入方式统一成：
   - 下载 `JSON/2LE`
   - 预处理成 `external constellation .mat`
   - 再由主程序读取 `.mat`

### 最优论文动作

如果面向 IEICE：
- 主对比写 `Starlink vs Qianfan`
- 车企相关性补充写 `GeeSat`

原因：
- `Starlink` 数据最好拿
- `Qianfan` 国内公开性最好
- `GeeSat` 最贴合车企，但自动化获取不如前两者顺手

## 7. 当前这个问题的最终结论

一句话总结：

`CelesTrak 仍然是我们当前最好的第一数据源，但如果论文想兼顾“国内”和“车企相关”，就不能只停留在 Starlink/OneWeb，必须把 Qianfan 和从 Active 总表派生出来的 GeeSat 一起纳入；而这些数据目前不能被现有 .mat 接口原样直接加载，必须先做一层外部星座配置转换。`
