# Tool Launcher Module - 工具启动器模块
# 完整功能版本

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QGridLayout, QMessageBox, QFileDialog,
    QLineEdit, QTabWidget, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
import os
import json
import subprocess


class CustomToolDialog(QDialog):
    """添加自定义软件对话框"""

    def __init__(self, tool_data=None, parent=None):
        super().__init__(parent)
        self.tool_data = tool_data or {}
        self.result = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("添加自定义软件")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 软件名称
        name_layout = QHBoxLayout()
        name_label = QLabel("软件名称:")
        name_label.setFont(QFont("Microsoft YaHei", 12))
        self.name_input = QLineEdit(self.tool_data.get("name", ""))
        self.name_input.setFont(QFont("Microsoft YaHei", 12))
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input, 1)
        layout.addLayout(name_layout)

        # 软件路径
        path_layout = QHBoxLayout()
        path_label = QLabel("软件路径:")
        path_label.setFont(QFont("Microsoft YaHei", 12))
        self.path_input = QLineEdit(self.tool_data.get("path", ""))
        self.path_input.setFont(QFont("Microsoft YaHei", 12))
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_file)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #616161; }
        """)
        btn_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept_data)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择可执行文件", "",
            "可执行文件 (*.exe *.bat *.cmd *.ps1 *.url);;所有文件 (*.*)"
        )
        if file_path:
            self.path_input.setText(file_path)
            if not self.name_input.text():
                self.name_input.setText(os.path.splitext(os.path.basename(file_path))[0])

    def accept_data(self):
        name = self.name_input.text().strip()
        path = self.path_input.text().strip()

        if not name:
            QMessageBox.warning(self, "警告", "请输入软件名称！")
            return
        if not path:
            QMessageBox.warning(self, "警告", "请选择软件路径！")
            return
        if not os.path.exists(path):
            QMessageBox.warning(self, "警告", "指定的文件不存在！")
            return

        self.result = {"name": name, "path": path}
        self.accept()


class ToolCard(QFrame):
    """工具卡片组件"""
    clicked = pyqtSignal(str)

    def __init__(self, tool_path, is_custom=False, tool_id=None):
        super().__init__()
        self.tool_path = tool_path
        self.is_custom = is_custom
        self.tool_id = tool_id

        if is_custom:
            self.tool_name = tool_path.get("name", "未知")
        else:
            self.tool_name = os.path.splitext(os.path.basename(tool_path))[0]

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 图标
        icon_label = QLabel("🔧" if not self.is_custom else "📦")
        icon_label.setFont(QFont("Arial", 32))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # 工具名称
        name_label = QLabel(self.tool_name)
        name_label.setFont(QFont("Microsoft YaHei", 11))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #333333;")
        name_label.setWordWrap(True)
        name_label.setMinimumHeight(40)
        layout.addWidget(name_label)

        # 样式
        self.setStyleSheet("""
            ToolCard {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
            ToolCard:hover {
                background-color: #f5f5f5;
                border: 1px solid #2196F3;
            }
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumSize(140, 140)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_custom and isinstance(self.tool_path, dict):
                self.clicked.emit(self.tool_path.get("path", ""))
            else:
                self.clicked.emit(self.tool_path)
        super().mousePressEvent(event)


class CategoryCard(QFrame):
    """分类卡片组件"""
    clicked = pyqtSignal(str)

    COLORS = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE"
    ]

    def __init__(self, category, tool_count, index):
        super().__init__()
        self.category = category
        self.tool_count = tool_count

        color = self.COLORS[index % len(self.COLORS)]
        self.setStyleSheet(f"""
            CategoryCard {{
                background-color: {color};
                border: none;
                border-radius: 16px;
                padding: 24px;
            }}
            CategoryCard:hover {{ opacity: 0.9; }}
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        icon_label = QLabel("📁")
        icon_label.setFont(QFont("Arial", 48))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        name_label = QLabel(self.category)
        name_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: white;")
        layout.addWidget(name_label)

        count_label = QLabel(f"{self.tool_count} 个工具")
        count_label.setFont(QFont("Microsoft YaHei", 12))
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("color: rgba(255,255,255,0.8);")
        layout.addWidget(count_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.category)
        super().mousePressEvent(event)


class ToolLauncherModule(BaseModule):
    """工具启动器模块"""
    module_name = "工具启动器"
    module_icon = "⚡"

    def __init__(self, parent=None):
        self.categories = []
        self.custom_tools = []
        self.current_category = None
        self.config_path = self._get_config_path()
        super().__init__(parent)

    def _get_config_path(self):
        """获取配置文件路径"""
        config_dir = os.path.join(self._find_project_root(), "config")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, "custom_tools.json")

    def _load_custom_tools(self):
        """加载自定义工具"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.custom_tools = json.load(f)
            except:
                self.custom_tools = []
        else:
            self.custom_tools = []

    def _save_custom_tools(self):
        """保存自定义工具"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.custom_tools, f, ensure_ascii=False, indent=2)

    def setup_ui(self):
        """设置模块UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        layout.setSpacing(SPACING["card"])

        # 标题
        title_label = QLabel(f"{self.module_icon} {self.module_name}")
        title_label.setFont(QFont(*FONTS["title_large"]))
        title_label.setStyleSheet(f"color: {COLORS['blue_dark']};")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFixedHeight(50)
        layout.addWidget(title_label)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { border: none; background-color: transparent; }
            QTabBar::tab {
                background-color: #f0f0f0;
                color: #666666;
                padding: 12px 40px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
            }
            QTabBar::tab:selected { background-color: #2196F3; color: white; }
            QTabBar::tab:hover:!selected { background-color: #e0e0e0; }
        """)

        # 内置工具标签页
        builtin_widget = QWidget()
        builtin_layout = QVBoxLayout(builtin_widget)
        builtin_layout.setContentsMargins(0, 0, 0, 0)
        builtin_layout.setSpacing(15)
        self._setup_builtin_tab(builtin_layout)
        self.tab_widget.addTab(builtin_widget, "🔧 内置工具")

        # 自定义软件标签页
        custom_widget = QWidget()
        custom_layout = QVBoxLayout(custom_widget)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.setSpacing(15)
        self._setup_custom_tab(custom_layout)
        self.tab_widget.addTab(custom_widget, "📦 自定义软件")

        layout.addWidget(self.tab_widget)

        # 加载数据
        self.load_tools()
        self._load_custom_tools()
        self.show_categories()

    def _setup_builtin_tab(self, layout):
        """设置内置工具标签页"""
        # 返回按钮
        self.back_button = QPushButton("← 返回分类")
        self.back_button.clicked.connect(self.show_categories)
        self.back_button.setVisible(False)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #616161; }
        """)
        layout.addWidget(self.back_button)

        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(20)

        self.scroll_area.setWidget(self.container)
        layout.addWidget(self.scroll_area)

    def _setup_custom_tab(self, layout):
        """设置自定义软件标签页"""
        # 工具栏
        toolbar_widget = QWidget()
        toolbar_widget.setStyleSheet("background-color: #f5f5f5; border-radius: 8px; padding: 12px;")
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        add_btn = QPushButton("➕ 添加软件")
        add_btn.clicked.connect(self.add_custom_tool)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        toolbar_layout.addWidget(add_btn)
        toolbar_layout.addStretch()
        layout.addWidget(toolbar_widget)

        # 滚动区域
        custom_scroll = QScrollArea()
        custom_scroll.setWidgetResizable(True)
        custom_scroll.setFrameShape(QFrame.NoFrame)

        self.custom_container = QWidget()
        self.custom_container_layout = QVBoxLayout(self.custom_container)
        self.custom_container_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_container_layout.setSpacing(20)

        custom_scroll.setWidget(self.custom_container)
        layout.addWidget(custom_scroll)

        self.refresh_custom_tools()

    def _find_project_root(self):
        """查找项目根目录"""
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        if os.path.exists(os.path.join(current_dir, "main.py")):
            return current_dir

        for _ in range(3):
            current_dir = os.path.dirname(current_dir)
            if os.path.exists(os.path.join(current_dir, "main.py")):
                return current_dir

        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def load_tools(self):
        """加载工具分类"""
        self.categories = []

        base_dir = self._find_project_root()

        tool_categories = [
            "内存工具", "处理器工具", "外设工具", "显卡工具",
            "显示器工具", "游戏工具", "烤鸡工具", "硬盘工具", "其他工具"
        ]

        for cat_name in tool_categories:
            cat_path = os.path.join(base_dir, cat_name)
            if os.path.isdir(cat_path):
                tools = self.load_tools_from_folder(cat_path)
                if tools:
                    self.categories.append({"name": cat_name, "path": cat_path, "tools": tools})

        # 如果没有找到预设分类，尝试扫描其他目录
        if not self.categories:
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path) and not item.startswith('.') and not item.startswith('_'):
                    if item.lower() not in ['src', '__pycache__', 'config']:
                        tools = self.load_tools_from_folder(item_path)
                        if tools:
                            self.categories.append({"name": item, "path": item_path, "tools": tools})

    def load_tools_from_folder(self, folder_path):
        """从文件夹加载工具"""
        tools = []

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                item_path = os.path.join(root, filename)
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.exe', '.bat', '.cmd', '.ps1', '.url']:
                    if not filename.startswith('.') and not filename.lower() in ['thumbs.db', 'desktop.ini']:
                        tools.append(item_path)

        return tools

    def clear_container(self, layout_obj=None):
        """清空容器"""
        layout = layout_obj or self.container_layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_categories(self):
        """显示分类页面"""
        self.current_category = None
        self.back_button.setVisible(False)
        self.clear_container()

        if not self.categories:
            no_tools_label = QLabel("没有找到工具分类\n请确保项目根目录下有工具文件夹")
            no_tools_label.setFont(QFont("Microsoft YaHei", 14))
            no_tools_label.setStyleSheet("color: #999999;")
            no_tools_label.setAlignment(Qt.AlignCenter)
            self.container_layout.addWidget(no_tools_label)
            self.container_layout.addStretch()
            return

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(20)

        for index, category in enumerate(self.categories):
            card = CategoryCard(category["name"], len(category["tools"]), index)
            card.clicked.connect(lambda _, cat=category["name"]: self.show_tools(cat))
            row = index // 3
            col = index % 3
            grid_layout.addWidget(card, row, col)

        for col in range(3):
            grid_layout.setColumnStretch(col, 1)

        self.container_layout.addWidget(grid_widget)
        self.container_layout.addStretch()

    def show_tools(self, category_name):
        """显示工具列表"""
        category = None
        for cat in self.categories:
            if cat["name"] == category_name:
                category = cat
                break

        if not category:
            return

        self.current_category = category
        self.back_button.setVisible(True)
        self.clear_container()

        # 标题行
        header_layout = QHBoxLayout()

        title_label = QLabel(category["name"])
        title_label.setFont(QFont("Microsoft YaHei", 22, QFont.Bold))
        title_label.setStyleSheet("color: #333333;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        open_folder_btn = QPushButton("📂 打开文件夹")
        open_folder_btn.clicked.connect(lambda: self.open_folder(category["path"]))
        open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        header_layout.addWidget(open_folder_btn)

        self.container_layout.addLayout(header_layout)

        count_label = QLabel(f"共 {len(category['tools'])} 个工具")
        count_label.setFont(QFont("Microsoft YaHei", 13))
        count_label.setStyleSheet("color: #666666; margin-bottom: 15px;")
        self.container_layout.addWidget(count_label)

        # 工具网格
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(18)

        for index, tool_path in enumerate(category["tools"]):
            card = ToolCard(tool_path)
            card.clicked.connect(self.launch_tool)
            row = index // 4
            col = index % 4
            grid_layout.addWidget(card, row, col)

        for col in range(4):
            grid_layout.setColumnStretch(col, 1)

        self.container_layout.addWidget(grid_widget)
        self.container_layout.addStretch()

    def refresh_custom_tools(self):
        """刷新自定义工具列表"""
        self.clear_container(self.custom_container_layout)

        if not self.custom_tools:
            empty_label = QLabel("还没有添加自定义软件\n点击上方的\"添加软件\"按钮来添加")
            empty_label.setFont(QFont("Microsoft YaHei", 14))
            empty_label.setStyleSheet("color: #999999;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.custom_container_layout.addWidget(empty_label)
            self.custom_container_layout.addStretch()
            return

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(18)

        for index, tool in enumerate(self.custom_tools):
            card = ToolCard(tool, is_custom=True, tool_id=index)
            card.clicked.connect(self.launch_tool)
            row = index // 4
            col = index % 4
            grid_layout.addWidget(card, row, col)

        for col in range(4):
            grid_layout.setColumnStretch(col, 1)

        self.custom_container_layout.addWidget(grid_widget)
        self.custom_container_layout.addStretch()

    def add_custom_tool(self):
        """添加自定义工具"""
        dialog = CustomToolDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            self.custom_tools.append(dialog.result)
            self._save_custom_tools()
            self.refresh_custom_tools()

    def launch_tool(self, tool_path):
        """启动工具"""
        try:
            if tool_path.endswith('.url'):
                os.startfile(tool_path)
            else:
                work_dir = os.path.dirname(tool_path)
                subprocess.Popen(tool_path, cwd=work_dir, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动工具失败：\n{str(e)}")

    def open_folder(self, folder_path):
        """打开文件夹"""
        try:
            os.startfile(folder_path)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"打开文件夹失败：\n{str(e)}")