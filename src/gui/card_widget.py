# Card Component - 卡片组件
# 统一的卡片式UI组件

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont
from .styles import COLORS, SPACING, FONTS


class CardWidget(QFrame):
    """
    基础卡片组件
    支持悬停效果、点击事件
    """
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(SPACING["card_padding"], SPACING["card_padding"], SPACING["card_padding"], SPACING["card_padding"])
        self.layout.setSpacing(10)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class InfoCard(CardWidget):
    """
    信息展示卡片
    用于显示硬件信息、统计数据等
    """
    def __init__(self, title="", subtitle="", icon="", parent=None):
        super().__init__(parent)
        self.info_text = ""
        if icon:
            self.info_text += icon + " "
        if title:
            self.info_text += title + "\n"
        if subtitle:
            self.info_text += subtitle
        
        self.label = QLabel(self.info_text)
        self.label.setFont(QFont("Microsoft YaHei", 12))
        self.label.setStyleSheet("color: #1a237e; background: transparent;")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        
    def set_title(self, text):
        self.title = text
        if self.title_label:
            self.title_label.setText(text)
            
    def set_subtitle(self, text):
        self.subtitle = text
        if self.subtitle_label:
            self.subtitle_label.setText(text)


class StatCard(CardWidget):
    """
    统计数据卡片
    用于显示数值、百分比、进度等
    """
    def __init__(self, title="", value="", unit="", icon="", color=COLORS["blue_main"], parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.unit = unit
        self.icon = icon
        self.color = color
        self.icon_label = None
        self.value_label = None
        self.title_label = None
        self.setup_stat_ui()
        
    def setup_stat_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Top row: icon + value
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        if self.icon:
            self.icon_label = QLabel(self.icon)
            self.icon_label.setFont(QFont("Arial", 32))
            self.icon_label.setStyleSheet(f"color: {self.color};")
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.icon_label.setFixedWidth(50)
            self.icon_label.setFixedHeight(50)
            top_layout.addWidget(self.icon_label)
            
        value_text = self.value
        if self.unit:
            value_text += f" {self.unit}"
        self.value_label = QLabel(value_text)
        self.value_label.setFont(QFont(*FONTS["title_large"]))
        self.value_label.setStyleSheet(f"color: {self.color}; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top_layout.addWidget(self.value_label, 1)
        
        main_layout.addLayout(top_layout)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont(*FONTS["body"]))
        self.title_label.setStyleSheet(f"color: {COLORS['gray_medium']};")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.title_label.setWordWrap(True)
        main_layout.addWidget(self.title_label)
        
        self.layout.addLayout(main_layout)
        
    def set_value(self, value):
        self.value = str(value)
        self.update_display()
        
    def update_display(self):
        value_text = self.value
        if self.unit:
            value_text += f" {self.unit}"
        if self.value_label:
            self.value_label.setText(value_text)


class SectionCard(QFrame):
    """
    分组卡片
    用于组织相关组件，带标题
    """
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS["white"]};
                border: 1px solid {COLORS["gray_border"]};
                border-radius: {SPACING["card_radius"]}px;
            }}
        """)
        self.setup_section_ui()
        
    def setup_section_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(SPACING["card_padding"], SPACING["card_padding"], SPACING["card_padding"], SPACING["card_padding"])
        main_layout.setSpacing(18)
        
        # Title
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont(*FONTS["title_small"]))
            title_label.setStyleSheet(f"color: {COLORS['blue_dark']}; border-bottom: 2px solid {COLORS['blue_main']}; padding-bottom: 12px; padding-top: 5px;")
            title_label.setWordWrap(True)
            main_layout.addWidget(title_label)
        
        # Content container
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(15)
        self.content_layout.setContentsMargins(5, 15, 5, 5)
        main_layout.addLayout(self.content_layout)
        
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)
        
    def add_layout(self, layout):
        self.content_layout.addLayout(layout)
