# 变更日志 (Changelog)

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/),
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-05-24

### 新增 (Added)
- ✨ 首次公开发布 v1.0.0
- 🖥️ PyQt5 图形界面启动器，支持暗色主题
- 📦 80+ 款专业便携工具集成
- 🔲 CPU 处理器检测与压力测试工具集
- 🎮 GPU 显卡检测与驱动管理工具集
- 💾 内存检测与稳定性测试工具集
- 💿 硬盘健康检测与性能基准工具集
- 🖥️ 显示器色域与坏点检测工具集
- 🖱️ 鼠标键盘外设测试工具集
- 🔥 整机压力测试（烤机）工具集
- 🎲 游戏平台与加速器工具集
- 🔧 系统维护实用工具集
- 🛡️ 内置功能模块：
  - 系统信息查看 (`system_info.py`)
  - 实时系统监控 (`system_monitor.py`)
  - 系统优化清理 (`system_optimizer.py`)
  - 进程管理器 (`task_manager.py`)
  - 注册表编辑器 (`registry_editor.py`)
  - 文件粉碎器 (`file_shredder.py`)
  - 文件浏览器 (`file_explorer.py`)
  - ISO 写入器 (`iso_writer.py`)
  - 驱动管理 (`driver_manager.py`)
  - 备份恢复 (`backup_restore.py`)
  - 网络诊断工具 (`network_tools.py`)
  - 安全扫描 (`security_scanner.py`)
  - 病毒扫描 (`virus_scanner.py`)
  - 工具启动器 (`tool_launcher.py`)
- 🎨 启动画面 (`splash_screen.py`)
- 📊 自定义仪表盘组件 (`gauge_widget.py`, `card_widget.py`)
- 🎨 统一暗色主题样式 (`styles.py`)
- 🔧 自定义工具扩展 (`custom_software.json`, `config/custom_tools.json`)
- 🪟 Windows 一键启动脚本 (`start.bat`)
- 📱 多尺寸 Logo 资源 (16x16 ~ 512x512 + 深色/浅色/单色变体)

### 技术栈
- UI: **PyQt5** + **PyQtChart**
- 系统: **psutil**, **pywin32**, **wmi**
- 语言: **Python 3.8+**
