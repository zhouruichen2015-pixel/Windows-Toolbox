# Gauge Widget - 简化版仪表盘组件

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class GaugeWidget(QWidget):
    """
    仪表盘组件 - 简化版
    """
    def __init__(self, title="", max_val=100, color="#2196F3", parent=None):
        super().__init__(parent)
        self.title = title
        self.max_val = max_val
        self.color = color
        self.current_value = 0
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Value display
        self.value_label = QLabel(f"{self.current_value}%")
        self.value_label.setFont(QFont("Microsoft YaHei", 32, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"color: {self.color};")
        layout.addWidget(self.value_label)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(self.max_val)
        self.progress.setValue(self.current_value)
        self.progress.setFormat("")
        self.progress.setFixedHeight(15)
        progress_style = f"""
            QProgressBar {{
                background-color: #e0e0e0;
                border-radius: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                border-radius: 8px;
            }}
        """
        self.progress.setStyleSheet(progress_style)
        layout.addWidget(self.progress)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Microsoft YaHei", 12))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #666666;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
    def set_value(self, value):
        self.current_value = min(max(int(value), 0), self.max_val)
        self.progress.setValue(self.current_value)
        self.value_label.setText(f"{self.current_value}%")