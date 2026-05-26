<div align="center">

<img src="assets/logo/zrc_logo_512x512.png" alt="ZRC工具箱 Logo" width="160" height="160" />

# 🛠️ ZRC 工具箱

**专业级 Windows 硬件检测与系统管理工具集**

[![Version](https://img.shields.io/badge/版本-v1.0.0-blue?style=for-the-badge&logo=github)](https://github.com/zhouruichen2015-pixel/ZRC-Toolbox/releases)
[![Platform](https://img.shields.io/badge/平台-Windows%207%2B-0078D7?style=for-the-badge&logo=windows)](https://github.com/zhouruichen2015-pixel/ZRC-Toolbox)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Tools](https://img.shields.io/badge/内置工具-80%2B-orange?style=for-the-badge)](https://github.com/zhouruichen2015-pixel/ZRC-Toolbox)
[![Stars](https://img.shields.io/github/stars/zhouruichen2015-pixel/ZRC-Toolbox?style=for-the-badge&color=yellow)](https://github.com/zhouruichen2015-pixel/ZRC-Toolbox/stargazers)

<br/>

> **一个启动器，驾驭所有硬件检测工具。**  
> 不再翻找文件夹，不再记路径——ZRC 工具箱让你在 3 秒内启动任何一款专业工具。

<br/>

[📥 立即下载](#-快速安装) · [🧭 功能一览](#-功能模块) · [📚 使用文档](#-使用指南) · [❓ 常见问题](#-常见问题)

</div>

> [!WARNING]
> **⚠️ 此仓库为源代码版（开发者版），不含 80+ 便携工具本体。**
> 普通用户请前往 **[Releases](../../releases/latest)** 下载完整版（4.7 GB，解压即用）。
> 开发者可 Clone 本仓库后按 [开发环境搭建](#-开发环境搭建) 安装依赖运行。



<!-- 搜索关键词：工具箱 硬件检测 便携工具 系统工具箱 Windows工具箱 装机必备 CPU测试 GPU测试 内存测试 磁盘检测 硬盘检测 显示器测试 便携软件 免安装工具 系统诊断 性能测试 压力测试 网络诊断 -->

---

## ✨ 为什么选择 ZRC 工具箱？

装机佬、硬件玩家、DIY 爱好者都有一个共同的烦恼：**各种工具散落在 N 个文件夹，找起来费时费力。**

ZRC 工具箱彻底解决了这个问题：

| 🎯 问题 | ✅ ZRC 的解决方案 |
|--------|----------------|
| 工具太多，找不到 | 分类整理，一键启动 |
| 不知道用哪款工具 | 清晰分类，功能说明一目了然 |
| 装了又忘在哪儿了 | 全部集中在工具箱，永远知道在哪 |
| 新手不知道从哪下手 | 详细说明 + 推荐工具标注 |
| 常用软件来回切换 | 自定义软件功能，添加你自己的工具 |

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────┐
│              ZRC 工具箱 启动器                │
│            (PyQt5 GUI Application)          │
├──────────┬──────────┬──────────┬────────────┤
│  🔧 核心  │  🎨 UI层  │  📦 工具  │  ⚙️ 配置   │
│ 模块引擎  │  组件库   │  启动器  │  自定义     │
├──────────┼──────────┼──────────┼────────────┤
│main_window│card_widget│tool_launcher│custom_  │
│splash_screen│gauge_widget│  .py   │tools.json │
│styles.py │base_module│         │           │
└──────────┴──────────┴──────────┴────────────┘
         │              │              
    ┌────┴────┐   ┌────┴────────┐
    │ 功能模块 │   │ 第三方便携工具  │
    ├─────────┤   ├─────────────┤
    │system_  │   │ CPU-Z       │
    │info     │   │ HWiNFO      │
    │monitor  │   │ GPU-Z       │
    │optimizer│   │ CrystalDisk │
    │task_mgr │   │ MemTest86   │
    │network_ │   │ ...80+ tools│
    │scanner  │   └─────────────┘
    │registry │
    │editor   │
    │virus_   │
    │scanner  │
    │file_    │
    │shredder │
    │iso_     │
    │writer   │
    │driver_  │
    │manager  │
    │backup_  │
    │restore  │
    │security │
    │_scanner │
    └─────────┘
```

**技术栈：**
- **UI框架**: `PyQt5` + `PyQtChart` — 原生级桌面体验
- **系统交互**: `psutil` + `pywin32` + `wmi` — 深度系统集成
- **启动方式**: `start.bat`(一键启动) / `python main.py`(开发者模式)
- **自定义扩展**: 编辑 `custom_tools.json` 即可添加自己的工具

## 🗂️ 工具分类总览

ZRC 工具箱收录 **9 大分类、80+ 款专业工具**，覆盖硬件检测到系统维护的全链路需求。

```
ZRC工具箱/
├── 🔲 处理器工具/     ← CPU 检测、压测、性能榨取
├── 🎮 显卡工具/       ← GPU 检测、驱动管理、显卡压测  
├── 💾 内存工具/       ← 内存频率检测、稳定性测试
├── 💿 硬盘工具/       ← 健康检测、性能基准、分区管理
├── 🖥️ 显示器工具/     ← 响应时间、色域、坏点检测
├── 🖱️ 外设工具/       ← 鼠标/键盘测试与校准
├── 🔥 烤鸡工具/       ← 整机压力测试烤机必备
├── 🎲 游戏工具/       ← 游戏平台、加速器、修改器
└── 🔧 其他工具/       ← 系统维护、数据恢复、实用小工具
```

---

## 🔲 处理器工具

> 专为 CPU 性能党打造。从基础信息读取到极限压力测试，应有尽有。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **CPU-Z** | CPU/主板/内存全面信息读取，装机验货必备 | ⭐⭐⭐⭐⭐ |
| **Core Temp** | 实时 CPU 温度监控，支持每核独立温度显示 | ⭐⭐⭐⭐⭐ |
| **Prime95** | 业界最严苛的 CPU 稳定性测试，超频验证标准 | ⭐⭐⭐⭐⭐ |
| **LinX** | LINPACK 算法 CPU 性能压测，速度快效果好 | ⭐⭐⭐⭐ |
| **ThrottleStop** | CPU 降压/功耗控制神器，笔记本必备 | ⭐⭐⭐⭐ |
| **wPrime** | 多线程浮点运算性能测试 | ⭐⭐⭐ |
| **SuperPi** | 经典单核性能测试，超频圈流行基准 | ⭐⭐⭐ |
| **C2CLatency** | CPU 核心间延迟检测，优化大小核调度 | ⭐⭐⭐ |
| **CPU 天梯图** | 快速查询 CPU 性能排名，选购参考利器 | ⭐⭐⭐⭐ |

> 💡 **超频必读**：超频后先跑 Prime95 的 Small FFTs 模式 30 分钟，温度不爆表且无报错才算基本稳定。

---

## 🎮 显卡工具

> 显卡性能释放、驱动问题排查、烤机测试全搞定。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **GPU-Z** | 显卡规格、显存带宽、传感器实时读取 | ⭐⭐⭐⭐⭐ |
| **DDU** | Display Driver Uninstaller，驱动彻底清除防冲突 | ⭐⭐⭐⭐⭐ |
| **MSI Afterburner** | 显卡超频、风扇曲线控制、帧数叠加显示 | ⭐⭐⭐⭐⭐ |
| **NVIDIA Inspector** | NVIDIA 驱动层面的参数精细调节 | ⭐⭐⭐⭐ |
| **NVIDIA Profile Inspector** | 驱动配置文件编辑，游戏专项优化 | ⭐⭐⭐⭐ |
| **FurMark** | 甜甜圈烤机，显卡极限温度/功耗测试 | ⭐⭐⭐⭐ |
| **GpuTest** | 多场景显卡 OpenGL 性能测试 | ⭐⭐⭐ |
| **DXVAChecker** | 硬件视频加速能力检测 | ⭐⭐⭐ |
| **显卡天梯图** | 显卡性能排名速查，买卡选卡神器 | ⭐⭐⭐⭐ |

> ⚠️ **使用 DDU 前请注意**：务必在安全模式下运行，断网操作，卸载完成后再安装新驱动。

---

## 💾 内存工具

> 内存超频党的专属工具库，从 SPD 信息读取到稳定性极限拷机。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **Thaiphoon Burner** | 内存颗粒 SPD 信息读取，识别马甲条真实颗粒 | ⭐⭐⭐⭐⭐ |
| **ZenTimings** | 实时读取 AMD 平台内存时序参数 | ⭐⭐⭐⭐⭐ |
| **TestMem5 (TM5)** | 目前最严苛的内存稳定性测试工具 | ⭐⭐⭐⭐⭐ |
| **MemTest64** | 轻量级内存测试，在 Windows 下运行 | ⭐⭐⭐⭐ |
| **MemTest** | 经典内存错误检测工具 | ⭐⭐⭐⭐ |
| **MemTestPro** | 专业版内存测试工具 | ⭐⭐⭐ |
| **魔方内存盘** | 将内存划分为虚拟磁盘，提升临时文件读写速度 | ⭐⭐⭐ |

---

## 💿 硬盘工具

> 你的数据安不安全？硬盘还能撑多久？全部用数据说话。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **CrystalDiskInfo** | 硬盘 S.M.A.R.T. 健康状态检测，寿命评估 | ⭐⭐⭐⭐⭐ |
| **CrystalDiskMark** | 硬盘顺序/随机读写速度基准测试 | ⭐⭐⭐⭐⭐ |
| **DiskGenius** | 分区管理、数据恢复、坏道扫描全功能 | ⭐⭐⭐⭐⭐ |
| **WizTree** | 磁盘空间占用可视化扫描，找大文件秒级完成 | ⭐⭐⭐⭐⭐ |
| **AS SSD Benchmark** | 专为 SSD 优化的性能测试工具 | ⭐⭐⭐⭐ |
| **ATTO Disk Benchmark** | 专业磁盘传输速率测试 | ⭐⭐⭐⭐ |
| **HD Tune** | 硬盘性能+健康状态+坏道扫描三合一 | ⭐⭐⭐⭐ |
| **SpaceSniffer** | 磁盘空间树形图可视化工具 | ⭐⭐⭐⭐ |
| **Defraggler** | SSD/HDD 碎片整理工具 | ⭐⭐⭐ |
| **魔方数据恢复** | 误删文件快速恢复 | ⭐⭐⭐⭐ |
| **FinalData** | 深度数据恢复，格式化后也能找回 | ⭐⭐⭐⭐ |
| **H2testw** | U 盘/存储卡容量真实性验证，防假容量 | ⭐⭐⭐⭐ |
| **LLFTOOL** | 低级格式化工具，顽固坏盘最后手段 | ⭐⭐⭐ |

---

## 🖥️ 显示器工具

> 你的屏幕真的达到标称参数了吗？用数据验证。

| 工具 | 用途 |
|------|------|
| **UFO 测试** | 在线显示器响应时间/刷新率可视化测试 |
| **在线屏幕测试** | 坏点检测、亮度均匀性、色彩还原测试 |
| **色域检测** | 显示器实际色域覆盖率检测 |

---

## 🖱️ 外设工具

> 鼠标抖动？键盘延迟？用数据量化你的外设性能。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **MouseTester** | 鼠标轨迹精确度、速度一致性图表化分析 | ⭐⭐⭐⭐⭐ |
| **MOUSERATE** | 鼠标轮询率实时检测（500Hz / 1000Hz / 4000Hz+） | ⭐⭐⭐⭐⭐ |
| **AresonMouseTest** | 多维鼠标性能综合测试 | ⭐⭐⭐⭐ |
| **Keyboard Test Utility** | 键盘按键测试，检测鬼键、漏键 | ⭐⭐⭐⭐ |
| **KeyTweak** | 键位重映射工具，改键无需硬件支持 | ⭐⭐⭐⭐ |
| **鼠标单击变双击测试器** | 检测鼠标微动连击问题 | ⭐⭐⭐⭐ |
| **在线外设测试中心** | 在线综合外设功能测试 | ⭐⭐⭐ |

---

## 🔥 烤鸡工具

> 整机稳定性验证，超频必经之路。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **FurMark** | 显卡极限压力测试，甜甜圈烤机经典 | ⭐⭐⭐⭐⭐ |
| **FurMark Win64** | 64位版本，支持更大显存测试 | ⭐⭐⭐⭐⭐ |
| **Prime95** | CPU 极限压测（与处理器工具共享） | ⭐⭐⭐⭐⭐ |

> 🌡️ **温度警戒线参考**：CPU 一般不超过 90°C，显卡一般不超过 85°C，NVMe SSD 不超过 70°C。

---

## 🎲 游戏工具

> 游戏平台汇总 + 加速器全家桶 + 实用辅助。

**游戏平台：**
- 🎮 **Steam** — PC 游戏最大平台
- ⚔️ **Battle.net** — 暴雪游戏启动器
- 🚀 **Epic Games** — 白嫖圣地
- 🎯 **EA App** — EA 官方平台

**加速器合集：**
- 斧牛加速器 / 迅游加速器 / 雷神加速器 / 迅雷加速器

**实用辅助：**
- 🌸 **风灵月影** — 游戏修改器，单机玩家福音
- 🕹️ **玩家动力** — 游戏资讯与优化工具
- 📊 **GameBuff** — 游戏帧率/温度监控叠加显示

---

## 🔧 其他工具

> 系统维护的百宝箱，解决各种奇奇怪怪的 Windows 问题。

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **Dism++** | Windows 系统优化神器，清理/精简/修复全能 | ⭐⭐⭐⭐⭐ |
| **Everything** | 全盘文件秒级搜索，Windows 自带搜索的百倍速度 | ⭐⭐⭐⭐⭐ |
| **Geek Uninstaller** | 强力软件卸载工具，清除注册表残留 | ⭐⭐⭐⭐⭐ |
| **Dism++ Win 镜像工具** | 下载微软官方 Windows 安装镜像 | ⭐⭐⭐⭐⭐ |
| **Rufus** | 启动 U 盘制作工具，支持 UEFI | ⭐⭐⭐⭐⭐ |
| **Ventoy** | 一个 U 盘塞多个系统镜像，多系统引导神器 | ⭐⭐⭐⭐⭐ |
| **DirectX Repair** | DirectX 组件修复，解决游戏 d3dx 报错 | ⭐⭐⭐⭐⭐ |
| **BlueScreenView** | 蓝屏死机原因分析，读取 minidump 文件 | ⭐⭐⭐⭐ |
| **Procexp (Process Explorer)** | 增强版任务管理器，进程树/DLL 查看 | ⭐⭐⭐⭐⭐ |
| **BatteryInfoView** | 笔记本电池健康度详细报告 | ⭐⭐⭐⭐ |
| **DesktopOK** | 桌面图标位置一键保存/恢复 | ⭐⭐⭐ |
| **ULTRA ISO** | ISO 镜像制作/编辑工具 | ⭐⭐⭐⭐ |
| **WinDbg** | Windows 调试器，高级蓝屏/崩溃分析 | ⭐⭐⭐ |
| **GifCam** | 轻量录屏 GIF 工具，录制演示一步到位 | ⭐⭐⭐⭐ |

---

## 🖥️ 软件界面

> ZRC 工具箱采用深蓝色专业风格 UI，侧边栏导航 + 卡片式工具布局。

**主界面布局：**

```
┌─────────────────────────────────────────────────────────────┐
│  📁 文件(F)    ❓ 帮助(H)                                   │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  ⚡ 工具启动器  │    ┌────────┐  ┌────────┐  ┌────────┐      │
│  💻 系统信息   │    │ CPU-Z  │  │ GPU-Z  │  │ CDI    │      │
│  📊 系统监控   │    └────────┘  └────────┘  └────────┘      │
│  ⚙️ 任务管理器  │    ┌────────┐  ┌────────┐  ┌────────┐      │
│  📁 文件浏览器  │    │Prime95 │  │FurMark │  │ DDU    │      │
│  🗑️ 文件粉碎器  │    └────────┘  └────────┘  └────────┘      │
│  🔑 注册表编辑  │                                              │
│  🦠 安全扫描   │         📦 自定义软件 ➕ 添加                │
│  💾 ISO 写入   │                                              │
│              │                                              │
│  v1.0.0      │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

**设计规范：**
- 🎨 主色调：深蓝 `#1565C0` + 亮蓝 `#2196F3`
- 📐 侧边栏宽度：240px，背景 `#2C3E50`
- 🃏 工具卡片：圆角 12px，悬停高亮动效
- 🔤 字体：微软雅黑，正文 14px

---


> 💡 **仅下载源代码？** 源代码版需要自行安装 Python 依赖，不含工具本体。**普通用户请下载下方分卷压缩包。**

## 📥 快速安装

> **⚠️ 文件较大（总计约 4.7 GB），因 GitHub Releases 单文件限制为 2 GB，本工具箱采用 7z 分卷压缩格式发布。**  
> 请按以下步骤依次下载所有分卷，然后一键合并解压即可。

### 📦 第一步：下载分卷文件

前往 [Releases 页面](https://github.com/zhouruichen2015-pixel/ZRC-Toolbox/releases) 下载以下 **3 个分卷文件**（必须全部下载，缺一不可）：

| # | 文件名 | 大小 | 状态 |
|---|--------|------|------|
| 1 | `ZRC工具箱_v1.0.0_part1.7z` | 1.90 GB | 🔴 必须 |
| 2 | `ZRC工具箱_v1.0.0_part2.7z` | 1.90 GB | 🔴 必须 |
| 3 | `ZRC工具箱_v1.0.0_part3.7z` | 909 MB | 🔴 必须 |

> 💡 **总计约 4.71 GB**，建议在网络良好的环境下下载。下载完成后请核对各分卷的文件大小是否与上表一致。

### 🧩 第二步：合并解压（超简单！）

#### 前置准备

- ✅ 安装 [7-Zip](https://7-zip.org/)（免费开源压缩软件）
- ✅ 将下载好的 **3 个分卷文件放在同一个文件夹内**

#### 方法 A：右键解压（推荐 ⭐ 最简单）

```
1. 打开存放分卷文件的文件夹
2. 找到 ZRC工具箱_v1.0.0_part1.7z（第一个分卷）
3. 右键点击它 → 选择 7-Zip → 点击「解压到当前文件夹」（或「提取到 ZRC工具箱_v1.0.0\」）
4. 等待解压完成（进度条走完即表示 3 个分卷自动合并完毕）✅
```

> 🎯 **关键点：只需要右键操作 part1 文件！**  
> 7-Zip 会自动识别同目录下的 part2 和 part3 并自动合并解压，无需手动拼接。

#### 方法 B：命令行解压

```bash
# 将 3 个分卷放在同一目录后，执行：
7z x ZRC工具箱_v1.0.0_part1.7z
# 或指定解压目标路径：
7z x ZRC工具箱_v1.0.0_part1.7z -oD:\ZRC工具箱
```

#### 方法 C：7-Zip 图形界面

```
1. 打开 7-Zip File Manager
2. 导航到存放分卷的文件夹
3. 单击选中 ZRC工具箱_v1.0.0_part1.7z
4. 点击工具栏上的「提取」按钮
5. 选择目标路径，确认开始
```

### 🚀 第三步：启动工具箱

解压完成后你会得到完整的 `ZRC工具箱` 文件夹：

```
ZRC工具箱/
├── start.bat          ← 双击这个启动！
├── main.py
├── run.py
├── 🔲 处理器工具/
├── 🎮 显卡工具/
├── ... (其余 80+ 工具)
```

```bash
# 双击运行：
start.bat

# 或命令行启动：
python main.py
```

> 📌 首次运行会自动检测 Python 环境。如未安装 Python，请前往 [python.org](https://www.python.org/downloads/) 下载，安装时**务必勾选 "Add Python to PATH"**。

---

### ❌ 常见下载/解压问题

<details>
<summary><b>Q: 解压时报错"无法打开文件作为压缩包"？</b></summary>

**A:** 这通常意味着分卷文件不完整或缺失：

1. **检查 3 个分卷是否都在同一文件夹**
2. **核对每个分卷的文件大小是否与 Release 页面一致**
3. 如果大小不一致 → 重新下载该分卷文件
4. 如果大小一致但仍然报错 → 尝试用 MD5 校验文件完整性

</details>

<details>
<summary><b>Q: 只下载了 part1 能解压吗？</b></summary>

**A:** ❌ 不能。7z 分卷格式要求所有分卷齐全才能正确解压，缺少任何一个都会导致失败。必须下载全部 3 个分卷。

</details>

<details>
<summary><b>Q: 解压速度很慢怎么办？</b></summary>

**A:**
- 目标盘如果是 HDD（机械硬盘），建议解压到 SSD 固态硬盘
- 确保 7-Zip 版本较新（推荐 23.01+）
- 关闭杀毒软件的实时扫描（会拖慢解压速度）

</details>

<details>
<summary><b>Q: 没有安装 7-Zip 可以用 WinRAR 吗？</b></summary>

**A:** 可以。WinRAR 同样支持 .7z 分卷格式的解压，操作方式相同：右键 part1 → 解压到当前文件夹。

</details>

---

### 方法二：Python 源码运行（开发者）

**第一步：确认 Python 版本**

```bash
python --version
# 需要 Python 3.8 或更高版本
```

如未安装，请前往 [python.org](https://www.python.org/downloads/) 下载，安装时**务必勾选 "Add Python to PATH"**。

**第二步：克隆仓库**

```bash
git clone https://github.com/zhouruichen2015-pixel/ZRC-Toolbox.git
cd ZRC-Toolkit
```

**第三步：安装依赖**

```bash
pip install -r requirements.txt
```

依赖清单：

```
PyQt5>=5.15.0      # GUI 框架
PyQtChart>=5.15.0  # 图表组件
psutil>=5.9.0      # 系统信息获取
pywin32>=306       # Windows API
wmi>=1.5.1         # Windows 管理接口
```

**第四步：启动程序**

```bash
python main.py
# 或直接双击 start.bat
```

---

### 方法三：打包可执行文件

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/logo/zrc_logo_256x256.ico main.py
# 生成的 .exe 在 dist/ 目录下
```

---

## 📚 使用指南

### 🚀 启动工具

1. 左侧侧边栏点击 **"⚡ 工具启动器"**
2. 选择你需要的工具分类（处理器/显卡/内存...）
3. 点击工具卡片即可**一键启动**

### ➕ 添加自定义软件

1. 点击 **"📦 自定义软件"** 标签
2. 点击 **"➕ 添加软件"**
3. 填写软件名称 → 点击"浏览..."选择 .exe 文件
4. 确定保存，下次直接在工具箱内启动

### 📊 实时系统监控

1. 点击侧边栏 **"📊 电脑配置数据大屏"**
2. 实时查看 CPU 占用率、内存使用、磁盘 I/O、网络速度
3. 数据每秒自动刷新

### 📁 打开工具所在目录

- 在工具卡片上点击 **"📂 打开文件夹"** 即可跳转到工具所在路径

---

## 📁 项目结构

```
ZRC工具箱/
├── 📄 main.py                     # 主程序入口
├── 📄 run.py                      # 备用启动脚本
├── 🪟 start.bat                   # Windows 一键启动脚本
├── 📋 requirements.txt            # Python 依赖清单
├── ⚙️ custom_software.json        # 自定义软件配置
├── src/                           # 源代码目录
│   └── gui/
│       ├── main_window.py         # 主窗口逻辑
│       ├── styles.py              # 全局样式定义
│       ├── base_module.py         # 模块基类
│       ├── card_widget.py         # 卡片 UI 组件
│       ├── splash_screen.py       # 启动画面
│       ├── tool_launcher.py       # 工具启动器核心
│       ├── system_monitor.py      # 系统监控模块
│       ├── task_manager.py        # 任务管理器
│       ├── file_explorer.py       # 文件浏览器
│       ├── registry_editor.py     # 注册表编辑器
│       ├── file_shredder.py       # 文件粉碎器
│       ├── virus_scanner.py       # 安全扫描
│       └── iso_writer.py          # ISO 写入工具
├── assets/                        # 资源文件
│   ├── logo/                      # ZRC Logo 全尺寸套装
│   ├── icons/                     # 图标资源
│   └── images/                    # 图片资源
├── config/                        # 配置文件
├── 🔲 处理器工具/                  # CPU 相关工具文件夹
├── 🎮 显卡工具/                    # GPU 相关工具文件夹
├── 💾 内存工具/                    # 内存相关工具文件夹
├── 💿 硬盘工具/                    # 硬盘相关工具文件夹
├── 🖥️ 显示器工具/                  # 显示器相关工具文件夹
├── 🖱️ 外设工具/                    # 外设相关工具文件夹
├── 🔥 烤鸡工具/                    # 压力测试工具文件夹
├── 🎲 游戏工具/                    # 游戏工具文件夹
└── 🔧 其他工具/                    # 其他实用工具文件夹
```

---

## 💻 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 7 64位 | Windows 10 / 11 |
| 处理器 | 双核 CPU | 四核及以上 |
| 内存 | 2 GB | 4 GB 及以上 |
| 硬盘空间 | 500 MB | 1 GB 及以上 |
| Python 版本 | 3.8 | 3.10+ |
| 显示分辨率 | 1024×768 | 1920×1080 |

---

## ❓ 常见问题

<details>
<summary><b>Q: 双击 start.bat 没有反应或一闪而过？</b></summary>

**A:** 通常是 Python 未安装或未加入 PATH 环境变量。

1. 打开 CMD，输入 `python --version`
2. 若提示"不是内部命令"，请重新安装 Python 并勾选 **"Add Python to PATH"**
3. 安装完成后重新双击 start.bat

</details>

<details>
<summary><b>Q: 提示缺少模块（ModuleNotFoundError）？</b></summary>

**A:** 运行以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

若网速慢可使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

</details>

<details>
<summary><b>Q: 点击工具卡片没有反应？</b></summary>

**A:** 可能原因：
1. 工具文件不存在（压缩包解压不完整）
2. 工具需要管理员权限 → 右键 start.bat 选择"以管理员身份运行"

</details>

<details>
<summary><b>Q: 杀毒软件报毒怎么办？</b></summary>

**A:** 部分硬件检测工具（如底层读取 SMART 信息的工具）会触发杀毒软件误报，这是正常现象。建议：
1. 将 ZRC 工具箱目录添加到杀毒软件白名单
2. 工具均来自官方渠道，可自行验证 MD5 哈希值

</details>

<details>
<summary><b>Q: 如何添加/删除自定义工具？</b></summary>

**A:** 
- 添加：界面内"自定义软件" → "添加软件"
- 删除：直接编辑 `config/custom_software.json`，删除对应条目后重启程序

</details>

<details>
<summary><b>Q: 烤机多久才算通过？</b></summary>

**A:** 通用标准：
- **快速验证**：FurMark 30分钟 + Prime95 30分钟，无报错无异常降频
- **严格验证**：TM5 内存测试 1 轮通过，Prime95 Blend 模式 8 小时

</details>

---

## ⚠️ 注意事项

> **请在使用前阅读以下重要说明**

- 🌡️ **烤机风险**：压力测试期间请实时监控硬件温度，CPU 超过 95°C 或显卡超过 90°C 请立即停止
- 🔒 **管理员权限**：部分工具（DDU、注册表编辑器等）需要管理员权限，请右键以管理员身份运行
- 💾 **数据安全**：使用数据恢复工具前，切勿向待恢复分区写入任何数据
- 🔧 **注册表操作**：修改注册表前请务必手动创建还原点
- 📜 **版权声明**：工具箱内收录的第三方工具版权归原作者所有，仅供个人学习使用，请勿用于商业用途

---

## 📊 技术栈

```
┌─────────────────────────────────────┐
│  语言        Python 3.8+            │
│  GUI框架     PyQt5 5.15+            │
│  图表库      PyQtChart              │
│  系统监控    psutil                 │
│  Windows API pywin32 + wmi          │
│  打包工具    PyInstaller（可选）     │
└─────────────────────────────────────┘
```

---

## 🗺️ 路线图

- [x] v1.0.0 — 工具启动器核心功能
- [x] v1.0.0 — 系统监控大屏
- [x] v1.0.0 — 任务管理器、文件浏览器
- [ ] v1.1.0 — 系统信息全面展示模块
- [ ] v1.1.0 — 系统优化向导
- [ ] v1.2.0 — 驱动管理模块
- [ ] v1.2.0 — 网络诊断工具集成
- [ ] v2.0.0 — 自动更新机制
- [ ] v2.0.0 — 工具健康度自检（检测工具是否仍存在）

---

## 📜 更新日志

### v1.0.0 (2026-05-18)

**🎉 初始发布**

- 完整收录 80+ 款硬件检测与系统工具
- PyQt5 现代化 UI，深蓝色专业风格
- 侧边栏导航 + 卡片式工具布局
- 自定义软件添加功能
- 系统实时监控大屏
- 工具一键启动 + 打开文件夹
- ZRC 专属 Logo 设计（多尺寸套装）

---

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/your-feature`
3. 提交变更：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

**贡献方向：**
- 🐛 提交 Bug 报告
- 💡 提出新工具或功能建议
- 🔧 修复已知问题
- 📚 完善文档说明

---

## 📄 免责声明

本工具箱集成的第三方工具均来自官方渠道，仅供学习研究和个人使用。使用工具所造成的任何后果（包括但不限于硬件损坏、数据丢失）由使用者自行承担。请遵守各工具的相关许可协议。

---

<div align="center">

**如果这个项目对你有帮助，请点一个 ⭐ Star 支持一下！**

[![GitHub Stars](https://img.shields.io/github/stars/zhouruichen2015-pixel/ZRC-Toolbox?style=social)](https://github.com/zhouruichen2015-pixel/ZRC-Toolbox)

Made with ❤️ by [zhouruichen2015-pixel](https://github.com/zhouruichen2015-pixel)

</div>
