# Splash Screen - 启动画面组件

from PyQt5.QtWidgets import QSplashScreen, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette

class SplashScreen(QSplashScreen):
    """
    启动画面 - 显示LOGO和程序名称
    """
    def __init__(self, logo_path=None):
        # 创建启动画面背景
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor("#ffffff"))  # 白色背景
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置布局
        self.setup_ui(logo_path)
        
        # 动画状态
        self.opacity = 1.0
        
    def setup_ui(self, logo_path):
        """
        设置启动画面UI
        """
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        # LOGO显示
        logo_label = QLabel()
        if logo_path and QPixmap(logo_path).isNull() is False:
            logo_pixmap = QPixmap(logo_path)
            # 调整LOGO大小
            scaled_logo = logo_pixmap.scaled(
                150, 150, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            logo_label.setPixmap(scaled_logo)
        else:
            # 如果没有LOGO，显示emoji图标
            logo_label.setText("📦")
            logo_label.setFont(QFont("Arial", 80))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # 程序名称
        name_label = QLabel("ZRC工具箱")
        name_label.setFont(QFont("Microsoft YaHei", 36, QFont.Bold))
        name_label.setStyleSheet("color: #1565C0;")  # 深蓝色
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # 副标题
        subtitle_label = QLabel("专业的系统工具集成平台")
        subtitle_label.setFont(QFont("Microsoft YaHei", 14))
        subtitle_label.setStyleSheet("color: #666666;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # 加载提示
        self.loading_label = QLabel("正在加载...")
        self.loading_label.setFont(QFont("Microsoft YaHei", 12))
        self.loading_label.setStyleSheet("color: #999999;")
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)
        
        # 底部间距
        layout.addStretch()
        
    def update_loading_text(self, text):
        """
        更新加载提示文字
        """
        self.loading_label.setText(text)
        self.repaint()
        
    def fade_out(self, duration=1000):
        """
        淡出动画
        """
        # 创建淡出动画
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # 动画结束后关闭
        animation.finished.connect(self.close)
        
        animation.start()
        self.animation = animation