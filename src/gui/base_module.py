# Base Module - 模块基类
# 所有功能模块的基类

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .styles import COLORS, SPACING, FONTS, apply_styles


class BaseModule(QWidget):
    """
    所有功能模块的基类
    """
    module_name = "Base Module"
    module_icon = "📦"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """
        设置模块UI - 子类应该重写此方法
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        layout.setSpacing(SPACING["card"])
        
        title_label = QLabel(f"{self.module_icon} {self.module_name}")
        title_label.setFont(QFont(*FONTS["title_large"]))
        title_label.setStyleSheet(f"color: {COLORS['blue_dark']};")
        layout.addWidget(title_label)
        
        info_label = QLabel("此模块正在开发中...")
        info_label.setFont(QFont(*FONTS["body"]))
        info_label.setStyleSheet(f"color: {COLORS['gray_medium']};")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
    def refresh_data(self):
        """
        刷新数据 - 子类可以重写
        """
        pass
        
    def on_module_enter(self):
        """
        当模块被激活时调用
        """
        self.refresh_data()
        
    def on_module_leave(self):
        """
        当模块被切换离开时调用
        """
        pass
