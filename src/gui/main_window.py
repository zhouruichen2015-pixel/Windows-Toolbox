# Main Window - 主窗口
# ZRC工具箱主窗口 - 新的侧边栏导航结构

import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QStackedWidget, QFrame, QMessageBox, QAction, QMenuBar, QFileDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QCursor, QIcon

from .styles import get_stylesheet, get_sidebar_stylesheet, COLORS, FONTS, SPACING
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard


# Module definitions - 模块定义 (按A-Z字母顺序，但工具启动器优先)
MODULES = [
    {"name": "工具启动器", "icon": "⚡", "import": "tool_launcher"},
    {"name": "系统信息", "icon": "💻", "import": "system_info"},
    {"name": "系统优化", "icon": "⚙️", "import": "system_optimizer"},
    {"name": "网络工具", "icon": "🌐", "import": "network_tools"},
    {"name": "备份恢复", "icon": "📦", "import": "backup_restore"},
    {"name": "驱动管理", "icon": "🔧", "import": "driver_manager"},
    {"name": "安全扫描", "icon": "🛡️", "import": "security_scanner"},
    {"name": "病毒查杀", "icon": "🦠", "import": "virus_scanner"},
    {"name": "电脑配置数据大屏", "icon": "📊", "import": "system_monitor"},
    {"name": "镜像写入U盘", "icon": "💾", "import": "iso_writer"},
    {"name": "文件粉碎", "icon": "🗑️", "import": "file_shredder"},
    {"name": "任务管理器", "icon": "🔄", "import": "task_manager"},
    {"name": "注册表修改器", "icon": "📝", "import": "registry_editor"},
    {"name": "资源管理器", "icon": "📁", "import": "file_explorer"}
]


class ZRCMainWindow(QMainWindow):
    """
    ZRC工具箱主窗口 - 新的侧边栏导航结构
    """
    def __init__(self):
        super().__init__()
        self.modules = {}
        self.current_module_index = 0
        self.init_window()
        self.setup_ui()
        self.create_menu_bar()
        
    def init_window(self):
        """
        初始化窗口设置
        """
        self.setWindowTitle("ZRC工具箱")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        self.setStyleSheet(get_stylesheet())
        
        # 设置窗口图标 - 使用ZRC专属Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo", "zrc_logo_32x32.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        else:
            self.setWindowIcon(QIcon.fromTheme("computer", QIcon("📦")))
        
    def setup_ui(self):
        """
        设置主UI - 侧边栏 + 内容区
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建侧边栏
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # 创建内容区
        content_area = self.create_content_area()
        main_layout.addWidget(content_area, 1)
        
        # 加载第一个模块
        self.load_module(0)
        
    def create_sidebar(self):
        """
        创建侧边栏导航
        """
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(get_sidebar_stylesheet())
        sidebar.setFixedWidth(240)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)
        
        # 侧边栏标题 - 使用LOGO图片
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(10)
        
        # LOGO图片 - 使用ZRC专属Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo", "zrc_logo_64x64.png")
        logo_label = QLabel()
        if os.path.exists(logo_path):
            from PyQt5.QtGui import QPixmap
            pixmap = QPixmap(logo_path)
            # 调整图片大小
            pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("📦")
            logo_label.setFont(QFont("Arial", 24))
        
        title_layout.addWidget(logo_label)
        
        # 标题文字
        title_label = QLabel("ZRC工具箱")
        title_label.setObjectName("sidebarTitle")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_layout.addWidget(title_label)
        
        title_widget = QWidget()
        title_widget.setLayout(title_layout)
        sidebar_layout.addWidget(title_widget)
        
        # 模块按钮列表
        self.sidebar_buttons = []
        for i, module in enumerate(MODULES):
            btn = QPushButton(f"{module['icon']}  {module['name']}")
            btn.setObjectName("sidebarItem")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, index=i: self.load_module(index))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons.append(btn)
            
        sidebar_layout.addStretch()
        
        # 版本信息
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet(f"color: rgba(255,255,255,0.5); padding: 15px; text-align: center;")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        return sidebar
        
    def create_content_area(self):
        """
        创建内容区域
        """
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        content_layout.setSpacing(SPACING["card"])
        
        # 使用QStackedWidget管理不同模块
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        return content_area
        
    def load_module(self, index):
        """
        加载指定索引的模块
        """
        # 先释放之前的模块
        if hasattr(self, 'current_module') and self.current_module:
            self.current_module.on_module_leave()
        
        # 更新按钮状态
        for i, btn in enumerate(self.sidebar_buttons):
            btn.setChecked(i == index)
            
        self.current_module_index = index
        module_info = MODULES[index]
        
        # 检查是否已加载此模块
        if index in self.modules:
            self.stacked_widget.setCurrentWidget(self.modules[index])
            self.current_module = self.modules[index]
            self.current_module.on_module_enter()
            return
            
        # 创建新模块
        try:
            module = self.create_module_by_name(module_info["import"])
            self.modules[index] = module
            self.stacked_widget.addWidget(module)
            self.stacked_widget.setCurrentWidget(module)
            self.current_module = module
            module.on_module_enter()
        except Exception as e:
            print(f"加载模块失败: {e}")
            self.show_module_placeholder(module_info)
            
    def create_module_by_name(self, module_name):
        """
        根据模块名称创建对应的模块实例
        """
        if module_name == "tool_launcher":
            from .tool_launcher import ToolLauncherModule
            return ToolLauncherModule()
        elif module_name == "system_info":
            from .system_info import SystemInfoModule
            return SystemInfoModule()
        elif module_name == "system_optimizer":
            from .system_optimizer import SystemOptimizerModule
            return SystemOptimizerModule()
        elif module_name == "network_tools":
            from .network_tools import NetworkToolsModule
            return NetworkToolsModule()
        elif module_name == "backup_restore":
            from .backup_restore import BackupRestoreModule
            return BackupRestoreModule()
        elif module_name == "driver_manager":
            from .driver_manager import DriverManagerModule
            return DriverManagerModule()
        elif module_name == "security_scanner":
            from .security_scanner import SecurityScannerModule
            return SecurityScannerModule()
        elif module_name == "system_monitor":
            from .system_monitor import SystemMonitorModule
            return SystemMonitorModule()
        elif module_name == "task_manager":
            from .task_manager import TaskManagerModule
            return TaskManagerModule()
        elif module_name == "file_explorer":
            from .file_explorer import FileExplorerModule
            return FileExplorerModule()
        elif module_name == "registry_editor":
            from .registry_editor import RegistryEditorModule
            return RegistryEditorModule()
        elif module_name == "file_shredder":
            from .file_shredder import FileShredderModule
            return FileShredderModule()
        elif module_name == "virus_scanner":
            from .virus_scanner import VirusScannerModule
            return VirusScannerModule()
        elif module_name == "iso_writer":
            from .iso_writer import IsoWriterModule
            return IsoWriterModule()
        else:
            from .base_module import BaseModule
            return BaseModule()
            
    def show_module_placeholder(self, module_info):
        """
        显示模块占位页面（开发中）
        """
        from .base_module import BaseModule
        
        placeholder = BaseModule()
        placeholder.module_name = module_info["name"]
        placeholder.module_icon = module_info["icon"]
        
        self.modules[self.current_module_index] = placeholder
        self.stacked_widget.addWidget(placeholder)
        self.stacked_widget.setCurrentWidget(placeholder)
        self.current_module = placeholder
        
    def create_menu_bar(self):
        """
        创建菜单栏
        """
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        exit_action = QAction("退出(&X)", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def show_about(self):
        """
        显示关于对话框
        """
        QMessageBox.about(self, "关于 ZRC工具箱",
                        "<h3>ZRC工具箱 v1.0.0</h3>"
                        "<p>专业的系统工具集成平台</p>"
                        "<p>为用户提供全面的系统管理和硬件检测工具</p>"
                        "<p><b>功能模块：</b></p>"
                        "<ul>"
                        "<li>⚡ 工具启动器 - 快速启动各类系统工具</li>"
                        "<li>💻 系统信息 - 全面硬件软件信息展示</li>"
                        "<li>⚙️ 系统优化 - 系统性能优化工具</li>"
                        "<li>🌐 网络工具 - 网络诊断和管理</li>"
                        "<li>📦 备份恢复 - 数据备份和恢复</li>"
                        "<li>🔧 驱动管理 - 驱动程序管理</li>"
                        "<li>🛡️ 安全扫描 - 系统安全检测</li>"
                        "<li>🦠 病毒查杀 - 病毒扫描功能</li>"
                        "<li>📊 电脑配置数据大屏 - 实时系统监控</li>"
                        "<li>💾 镜像写入U盘 - ISO镜像烧录</li>"
                        "<li>🗑️ 文件粉碎 - 安全删除文件</li>"
                        "<li>🔄 任务管理器 - 进程管理</li>"
                        "<li>📝 注册表修改器 - 高级系统配置</li>"
                        "<li>📁 资源管理器 - 文件浏览管理</li>"
                        "</ul>"
                        "<p><b>技术支持：</b>ZRC Development Team</p>")
