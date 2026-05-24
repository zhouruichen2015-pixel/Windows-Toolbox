# Driver Manager Module - 驱动管理模块
# 提供驱动程序管理功能

import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
from .card_widget import SectionCard, StatCard


class DriverManagerModule(BaseModule):
    """驱动管理模块 - 提供驱动程序管理功能"""
    
    module_name = "驱动管理"
    module_icon = "🔧"
    
    def setup_ui(self):
        """设置模块UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        main_layout.setSpacing(SPACING["card"])
        
        # 标题
        title = QLabel(f"{self.module_icon} {self.module_name}")
        title.setFont(QFont(*FONTS["title_large"]))
        title.setStyleSheet(f"color: {COLORS['blue_dark']};")
        main_layout.addWidget(title)
        
        # 标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 已安装驱动
        self.create_installed_drivers_tab()
        
        # 驱动更新
        self.create_update_tab()
    
    def create_installed_drivers_tab(self):
        """创建已安装驱动标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("已安装驱动列表")
        
        self.driver_list = QListWidget()
        self.driver_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
            }}
        """)
        section.add_widget(self.driver_list)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.load_drivers)
        button_layout.addWidget(refresh_btn)
        
        section.add_layout(button_layout)
        
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "📋 已安装驱动")
        
        # 加载驱动列表
        self.load_drivers()
    
    def create_update_tab(self):
        """创建驱动更新标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("驱动更新")
        
        # 提示信息
        info_label = QLabel("驱动更新功能需要通过Windows更新或厂商官方工具进行。")
        info_label.setFont(QFont(*FONTS["body"]))
        info_label.setStyleSheet(f"color: {COLORS['gray_medium']};")
        section.add_widget(info_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        win_update_btn = QPushButton("🪟 打开Windows更新")
        win_update_btn.clicked.connect(self.open_windows_update)
        button_layout.addWidget(win_update_btn)
        
        device_manager_btn = QPushButton("⚙️ 打开设备管理器")
        device_manager_btn.clicked.connect(self.open_device_manager)
        button_layout.addWidget(device_manager_btn)
        
        section.add_layout(button_layout)
        
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "🔄 驱动更新")
    
    def load_drivers(self):
        """加载已安装驱动列表"""
        self.driver_list.clear()
        try:
            # 添加提示信息
            info_item = QListWidgetItem("💡 提示: 请使用设备管理器查看详细驱动信息")
            info_item.setForeground(Qt.blue)
            self.driver_list.addItem(info_item)
            
            info_item2 = QListWidgetItem("⚠️ 部分功能需要管理员权限")
            info_item2.setForeground(Qt.darkYellow)
            self.driver_list.addItem(info_item2)
            
            self.driver_list.addItem("")  # 空行分隔
            
            # 先尝试用PowerShell获取基本驱动信息（不需要管理员权限）
            try:
                result = subprocess.check_output(
                    ["powershell", "-Command", 
                     "Get-PnpDevice | Where-Object {$_.Status -eq 'OK'} | Select-Object FriendlyName, Class, Status | ConvertTo-Json -Compress"],
                    text=True,
                    timeout=30
                )
                import json
                drivers = json.loads(result)
                count = 0
                if isinstance(drivers, list):
                    for driver in drivers:
                        name = driver.get('FriendlyName', 'Unknown')
                        cls = driver.get('Class', 'Unknown')
                        status = driver.get('Status', 'Unknown')
                        list_item = QListWidgetItem(f"📦 {name}\n  [{cls}] - {status}")
                        self.driver_list.addItem(list_item)
                        count += 1
                        if count >= 50:  # 只显示前50个
                            break
                else:
                    name = drivers.get('FriendlyName', 'Unknown')
                    cls = drivers.get('Class', 'Unknown')
                    status = drivers.get('Status', 'Unknown')
                    list_item = QListWidgetItem(f"📦 {name}\n  [{cls}] - {status}")
                    self.driver_list.addItem(list_item)
            except Exception as e1:
                # 如果PowerShell失败，使用wmic获取
                try:
                    result = subprocess.check_output(
                        ["wmic", "path", "win32_pnpsigneddriver", "get", "DeviceName,DriverVersion,Manufacturer"],
                        text=True,
                        timeout=30
                    )
                    lines = result.strip().split('\n')[1:]  # 跳过标题行
                    if len(lines) > 0:
                        self.driver_list.addItem("--- 已签名驱动列表 ---")
                        for line in lines[:50]:  # 只显示前50个
                            if line.strip():
                                parts = [p.strip() for p in line.split('  ') if p.strip()]
                                if len(parts) >= 3:
                                    name = parts[0]
                                    version = parts[1]
                                    manufacturer = parts[2]
                                    list_item = QListWidgetItem(f"📦 {name}\n  厂商: {manufacturer} | 版本: {version}")
                                    self.driver_list.addItem(list_item)
                    else:
                        self.driver_list.addItem("暂无已签名驱动信息")
                except Exception as e2:
                    self.driver_list.addItem("")
                    self.driver_list.addItem("🔧 推荐使用设备管理器查看详细驱动")
                    self.driver_list.addItem("   点击下方按钮打开设备管理器")
        except Exception as e:
            self.driver_list.addItem("")
            self.driver_list.addItem(f"❌ 获取驱动列表失败: {str(e)}")
            self.driver_list.addItem("")
            self.driver_list.addItem("🔧 推荐使用设备管理器查看详细驱动")
    
    def open_windows_update(self):
        """打开Windows更新"""
        try:
            subprocess.run(["ms-settings:windowsupdate"], check=True)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法打开Windows更新: {str(e)}")
    
    def open_device_manager(self):
        """打开设备管理器"""
        try:
            subprocess.run(["devmgmt.msc"], check=True)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法打开设备管理器: {str(e)}")