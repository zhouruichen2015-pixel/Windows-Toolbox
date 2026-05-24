# 贡献指南 (Contributing)

感谢你对 ZRC 工具箱的关注！欢迎以各种方式参与项目。

## 🤝 如何贡献

### 报告 Bug
- 使用 [Issues](../../issues) 提交问题
- 标题格式：`[Bug] 简要描述`
- 请包含：复现步骤、预期行为、实际行为、环境信息（Windows 版本、Python 版本）

### 提出新功能
- 使用 [Issues](../../issues) 提出 Feature Request
- 标题格式：`[Feature] 功能名称`
- 说明使用场景和期望效果

### 提交代码
1. **Fork 本仓库**
2. **创建分支**: `git checkout -b feature/你的功能名`
3. **提交更改**: `git commit -m 'feat: 添加xxx功能'`
4. **推送分支**: `git push origin feature/你的功能名`
5. **创建 Pull Request**

### Commit 规范
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具链

## 🔧 开发环境搭建

```bash
# 1. 克隆仓库
git clone https://github.com/zhouruichen2015-pixel/ZRC-Toolbox.git
cd ZRC-Toolbox

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python main.py
# 或
start.bat
```

**依赖要求：**
- Python >= 3.8
- PyQt5 >= 5.15.0
- PyQtChart >= 5.15.0
- psutil >= 5.9.0
- pywin32 >= 306
- wmi >= 1.5.1

## 📋 代码规范

- 遵循 PEP 8 风格指南
- 注释使用中文
- 新增功能模块放在 `src/gui/` 下
- 自定义工具配置在 `config/custom_tools.json`

## ⚠️ 注意事项

- 本项目仅支持 Windows 平台
- GUI 基于 PyQt5，确保熟悉 Qt 信号槽机制
- 系统交互使用了 `psutil`、`wmi` 和 `pywin32`
