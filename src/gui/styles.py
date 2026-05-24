# Blue and White Style System
# MHY工具箱统一UI设计系统 - 蓝白色调配色方案

# Colors - 蓝白色调配色方案
COLORS = {
    # Blue palette - 蓝色系主色调
    "blue_light": "#E3F2FD",
    "blue_main": "#2196F3",
    "blue_dark": "#1565C0",
    "blue_hover": "#1976D2",
    "blue_dark_bg": "#2C3E50",
    
    # White palette - 白色系辅助色
    "white": "#FFFFFF",
    "gray_light": "#FAFAFA",
    "gray_dark": "#333333",
    "gray_medium": "#666666",
    "gray_border": "#E0E0E0",
    
    # Status colors - 状态色
    "success": "#4CAF50",
    "warning": "#FF9800",
    "danger": "#F44336"
}

# Fonts - 字体设置
FONTS = {
    "family": "Microsoft YaHei, Arial, sans-serif",
    "title_large": ("Microsoft YaHei", 24, True),
    "title_medium": ("Microsoft YaHei", 20, True),
    "title_small": ("Microsoft YaHei", 16, True),
    "body": ("Microsoft YaHei", 14),
    "body_small": ("Microsoft YaHei", 12),
    "auxiliary": ("Microsoft YaHei", 10)
}

# Spacing - 间距规范
SPACING = {
    "card": 20,
    "card_padding": 16,
    "card_radius": 12,
    "input_radius": 8,
    "button_radius": 8
}

# Main Stylesheet - 主样式表
MAIN_STYLESHEET = f"""
/* Base Application Styles */
QMainWindow {{
    background-color: {COLORS["gray_light"]};
}}

QWidget {{
    font-family: {FONTS["family"]};
    color: {COLORS["gray_dark"]};
}}

/* Card Component - 卡片组件 */
CardWidget, QFrame.card {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["card_radius"]}px;
    padding: {SPACING["card_padding"]}px;
}}

CardWidget:hover, QFrame.card:hover {{
    border: 1px solid {COLORS["blue_main"]};
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}}

/* Buttons - 按钮样式 */
QPushButton {{
    background-color: {COLORS["blue_main"]};
    color: {COLORS["white"]};
    border: none;
    border-radius: {SPACING["button_radius"]}px;
    padding: 8px 16px;
    font-size: 14px;
    font-family: {FONTS["family"]};
}}

QPushButton:hover {{
    background-color: {COLORS["blue_hover"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["blue_dark"]};
}}

QPushButton:disabled {{
    background-color: {COLORS["gray_border"]};
    color: {COLORS["gray_medium"]};
}}

/* Secondary Button - 次按钮样式 */
QPushButton.secondary {{
    background-color: {COLORS["white"]};
    color: {COLORS["blue_main"]};
    border: 1px solid {COLORS["blue_main"]};
}}

QPushButton.secondary:hover {{
    background-color: {COLORS["blue_light"]};
}}

/* Danger Button - 危险按钮 */
QPushButton.danger {{
    background-color: {COLORS["danger"]};
}}

QPushButton.danger:hover {{
    background-color: #D32F2F;
}}

/* Success Button - 成功按钮 */
QPushButton.success {{
    background-color: {COLORS["success"]};
}}

QPushButton.success:hover {{
    background-color: #388E3C;
}}

/* Input Fields - 输入框样式 */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["input_radius"]}px;
    padding: 8px 12px;
    font-size: 14px;
    font-family: {FONTS["family"]};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {COLORS["blue_main"]};
}}

/* Combo Box - 下拉框 */
QComboBox {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["input_radius"]}px;
    padding: 8px 12px;
    font-size: 14px;
    font-family: {FONTS["family"]};
}}

QComboBox:focus {{
    border: 2px solid {COLORS["blue_main"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {COLORS["gray_dark"]};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    selection-background-color: {COLORS["blue_light"]};
    selection-color: {COLORS["blue_dark"]};
}}

/* Table Styles - 表格样式 */
QTableWidget, QTableView {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    gridline-color: {COLORS["gray_border"]};
    selection-background-color: {COLORS["blue_light"]};
    selection-color: {COLORS["blue_dark"]};
}}

QHeaderView::section {{
    background-color: {COLORS["blue_light"]};
    color: {COLORS["blue_dark"]};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {COLORS["blue_main"]};
    font-weight: bold;
    font-family: {FONTS["family"]};
}}

QTableWidget::item:hover, QTableView::item:hover {{
    background-color: #F5F9FF;
}}

QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {COLORS["blue_light"]};
    color: {COLORS["blue_dark"]};
}}

/* List Widget - 列表组件 */
QListWidget {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["input_radius"]}px;
}}

QListWidget::item {{
    padding: 10px;
    border-radius: 6px;
}}

QListWidget::item:hover {{
    background-color: {COLORS["blue_light"]};
}}

QListWidget::item:selected {{
    background-color: {COLORS["blue_main"]};
    color: {COLORS["white"]};
}}

/* Tree Widget - 树形组件 */
QTreeWidget {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["input_radius"]}px;
}}

QTreeWidget::item {{
    padding: 8px;
}}

QTreeWidget::item:hover {{
    background-color: {COLORS["blue_light"]};
}}

QTreeWidget::item:selected {{
    background-color: {COLORS["blue_main"]};
    color: {COLORS["white"]};
}}

QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {{
    border-image: none;
    image: none;
}}

QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {{
    border-image: none;
    image: none;
}}

/* Scrollbar - 滚动条样式 */
QScrollBar:vertical {{
    background-color: {COLORS["gray_light"]};
    width: 10px;
    border-radius: 5px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["gray_border"]};
    min-height: 30px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["blue_main"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: {COLORS["gray_light"]};
    height: 10px;
    border-radius: 5px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS["gray_border"]};
    min-width: 30px;
    border-radius: 5px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS["blue_main"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* Tab Widget - 标签页 */
QTabWidget::pane {{
    border: 1px solid {COLORS["gray_border"]};
    background-color: {COLORS["white"]};
}}

QTabBar::tab {{
    background-color: {COLORS["gray_light"]};
    color: {COLORS["gray_medium"]};
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS["white"]};
    color: {COLORS["blue_main"]};
    border: 1px solid {COLORS["gray_border"]};
    border-bottom: none;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS["blue_light"]};
}}

/* Checkbox - 复选框 */
QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS["gray_border"]};
    border-radius: 4px;
    background-color: {COLORS["white"]};
}}

QCheckBox::indicator:hover {{
    border: 2px solid {COLORS["blue_main"]};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS["blue_main"]};
    border: 2px solid {COLORS["blue_main"]};
    image: url(:/icons/check.svg);
}}

/* Radio Button - 单选框 */
QRadioButton {{
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS["gray_border"]};
    border-radius: 9px;
    background-color: {COLORS["white"]};
}}

QRadioButton::indicator:hover {{
    border: 2px solid {COLORS["blue_main"]};
}}

QRadioButton::indicator:checked {{
    background-color: {COLORS["white"]};
    border: 2px solid {COLORS["blue_main"]};
}}

QRadioButton::indicator::checked::indicator {{
    width: 10px;
    height: 10px;
    background-color: {COLORS["blue_main"]};
    border-radius: 5px;
    margin: 4px;
}}

/* Progress Bar - 进度条 */
QProgressBar {{
    background-color: {COLORS["gray_border"]};
    border-radius: 10px;
    text-align: center;
    color: {COLORS["white"]};
    font-weight: bold;
    height: 20px;
}}

QProgressBar::chunk {{
    background-color: {COLORS["blue_main"]};
    border-radius: 10px;
}}

/* Group Box - 分组框 */
QGroupBox {{
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["card_radius"]}px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
    color: {COLORS["blue_dark"]};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 5px;
}}

/* Slider - 滑块 */
QSlider::groove:horizontal {{
    height: 6px;
    background: {COLORS["gray_border"]};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {COLORS["blue_main"]};
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {COLORS["blue_hover"]};
}}

/* Spin Box - 数字输入框 */
QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: {SPACING["input_radius"]}px;
    padding: 6px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {COLORS["blue_main"]};
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid {COLORS["gray_border"]};
    background: {COLORS["gray_light"]};
}}

QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid {COLORS["gray_border"]};
    border-top: 1px solid {COLORS["gray_border"]};
    background: {COLORS["gray_light"]};
}}

/* Menu - 菜单 */
QMenu {{
    background-color: {COLORS["white"]};
    border: 1px solid {COLORS["gray_border"]};
    border-radius: 8px;
    padding: 8px 0;
}}

QMenu::item {{
    padding: 8px 30px;
}}

QMenu::item:selected {{
    background-color: {COLORS["blue_light"]};
    color: {COLORS["blue_dark"]};
}}

QMenu::separator {{
    height: 1px;
    background: {COLORS["gray_border"]};
    margin: 5px 10px;
}}

/* Status Bar - 状态栏 */
QStatusBar {{
    background-color: {COLORS["white"]};
    border-top: 1px solid {COLORS["gray_border"]};
    color: {COLORS["gray_medium"]};
}}

/* Tool Tip - 工具提示 */
QToolTip {{
    background-color: {COLORS["gray_dark"]};
    color: {COLORS["white"]};
    border: none;
    padding: 8px 12px;
    border-radius: 6px;
}}
"""

# Sidebar Styles - 侧边栏样式
SIDEBAR_STYLESHEET = f"""
/* Sidebar Container */
QWidget#sidebar {{
    background-color: {COLORS["blue_dark_bg"]};
}}

/* Sidebar Title */
QLabel#sidebarTitle {{
    color: {COLORS["white"]};
    font-size: 18px;
    font-weight: bold;
    padding: 20px;
    background-color: transparent;
}}

/* Sidebar Navigation Items */
QPushButton#sidebarItem {{
    background-color: transparent;
    color: {COLORS["white"]};
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    border-radius: 8px;
    margin: 4px 10px;
}}

QPushButton#sidebarItem:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}

QPushButton#sidebarItem:checked, QPushButton#sidebarItem.selected {{
    background-color: {COLORS["blue_main"]};
    color: {COLORS["white"]};
}}

QPushButton#sidebarItem:checked:hover, QPushButton#sidebarItem.selected:hover {{
    background-color: {COLORS["blue_hover"]};
}}

/* Sidebar Icons */
QLabel#sidebarIcon {{
    color: {COLORS["white"]};
    font-size: 20px;
    margin-right: 10px;
}}
"""


def get_stylesheet():
    """
    获取完整的主样式表
    """
    return MAIN_STYLESHEET


def get_sidebar_stylesheet():
    """
    获取侧边栏样式表
    """
    return SIDEBAR_STYLESHEET


def apply_styles(widget):
    """
    为指定组件应用统一样式
    """
    widget.setStyleSheet(MAIN_STYLESHEET)
