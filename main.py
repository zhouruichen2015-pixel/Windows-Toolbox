# ZRC工具箱 - 主程序入口
# 集成系统工具的专业工具箱

import sys
import os
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# 确保导入路径正确
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.gui.main_window import ZRCMainWindow
from src.gui.splash_screen import SplashScreen


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setStyle('Fusion')
    
    # LOGO文件路径
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo', 'zrc_logo_512x512.png')
    
    # 创建并显示启动画面
    splash = SplashScreen(logo_path)
    splash.show()
    
    # 模拟加载过程
    loading_steps = [
        "正在初始化界面...",
        "正在加载模块...",
        "正在准备工具...",
        "启动完成！"
    ]
    
    for step in loading_steps:
        splash.update_loading_text(step)
        app.processEvents()
        time.sleep(0.7)
    
    # 创建主窗口
    window = ZRCMainWindow()
    
    # 显示主窗口后关闭启动画面
    def show_main_window():
        window.show()
        splash.fade_out(duration=800)
    
    # 延迟一点时间让启动画面完全显示
    QTimer.singleShot(200, show_main_window)
    
    # 进入主事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
