# Assets 资源目录

本目录存放ZRC工具箱的所有资源文件。

## 目录结构

```
assets/
├── README.md                    # 本文件
├── logo/                        # Logo相关资源
│   ├── README.md               # Logo设计说明
│   ├── zrc_logo_512x512.png    # 主Logo（512x512）
│   ├── zrc_logo_256x256.png    # Logo（256x256）
│   ├── zrc_logo_128x128.png    # Logo（128x128）
│   ├── zrc_logo_64x64.png      # Logo（64x64）
│   ├── zrc_logo_32x32.png      # Logo（32x32）
│   ├── zrc_logo_16x16.png      # Logo（16x16）
│   ├── zrc_logo_256x256.ico    # Windows图标格式
│   ├── zrc_logo.svg            # 矢量格式
│   ├── zrc_logo_white_bg.png   # 白色背景版本
│   ├── zrc_logo_dark_bg.png    # 深色背景版本
│   └── zrc_logo_monochrome.png # 单色版本
├── icons/                       # 图标资源
│   └── README.md
└── images/                      # 其他图片资源
    └── README.md
```

## Logo 设计规范

### 设计理念

ZRC工具箱Logo采用蓝白几何风格设计：

- **主色调**：深蓝色(#1565C0) + 亮蓝色(#2196F3)
- **辅助色**：白色(#FFFFFF)
- **设计元素**：字母ZRC + 工具箱/齿轮图形

### 文件说明

| 文件 | 尺寸 | 用途 |
|------|------|------|
| zrc_logo_512x512.png | 512x512 | 主要Logo、大尺寸显示 |
| zrc_logo_256x256.png | 256x256 | 中等尺寸显示 |
| zrc_logo_128x128.png | 128x128 | 小尺寸显示 |
| zrc_logo_64x64.png | 64x64 | 图标显示 |
| zrc_logo_32x32.png | 32x32 | 窗口标题栏 |
| zrc_logo_16x16.png | 16x16 | 任务栏小图标 |
| zrc_logo_256x256.ico | 256x256 | Windows可执行文件图标 |
| zrc_logo.svg | 矢量 | 无限缩放、打印 |

### 使用规范

1. **最小尺寸**：Logo显示不应小于16x16px
2. **安全边距**：Logo周围应保留至少高度1/4的空白
3. **颜色使用**：
   - 白色/浅色背景 → 使用标准Logo
   - 深色背景 → 使用zrc_logo_dark_bg.png
   - 需要单色 → 使用zrc_logo_monochrome.png
4. **禁止行为**：
   - 拉伸、压缩、改变比例
   - 修改颜色
   - 添加额外元素
   - 旋转或倾斜

## 注意事项

- 本目录下的资源文件请不要随意删除
- 如需替换Logo，请保持文件名一致
- 建议使用矢量SVG格式进行设计修改
