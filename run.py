#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZRC 工具箱 - 正式启动脚本
该脚本提供了错误处理，在启动失败时显示友好的提示信息
"""

import sys
import os

# 确保当前目录在路径中，这样可以正确导入项目模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # 导入主程序入口函数
    from src.gui.main_window import main
    if __name__ == '__main__':
        # 启动主程序
        main()
except ImportError as e:
    # 处理导入错误（通常是缺少依赖）
    print(f"导入错误: {e}")
    print("请确保已安装所有依赖: pip install -r requirements.txt")
    input("按回车键退出...")
except Exception as e:
    # 处理其他类型的启动错误
    print(f"程序启动失败: {e}")
    import traceback
    traceback.print_exc()
    input("按回车键退出...")
