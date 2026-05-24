# Network Tools Module - 网络工具模块
# 提供网络诊断和管理功能

import os
import subprocess
import socket
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QTextEdit, QLineEdit, QProgressBar,
    QListWidget, QListWidgetItem, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
from .card_widget import SectionCard, StatCard


class PingThread(QThread):
    """Ping测试线程"""
    result = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, host, count=4):
        super().__init__()
        self.host = host
        self.count = count
    
    def run(self):
        try:
            result = subprocess.run(
                ["ping", "-n", str(self.count), self.host],
                text=True,
                timeout=30
            )
            self.result.emit(result.stdout)
        except subprocess.TimeoutExpired:
            self.result.emit("Ping超时")
        except Exception as e:
            self.result.emit(f"Ping失败: {str(e)}")
        finally:
            self.finished.emit()


class NetworkToolsModule(BaseModule):
    """网络工具模块 - 提供网络诊断和管理功能"""
    
    module_name = "网络工具"
    module_icon = "🌐"
    
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
        
        # 网络状态
        self.create_status_tab()
        
        # Ping测试
        self.create_ping_tab()
        
        # 网络信息
        self.create_info_tab()
    
    def create_status_tab(self):
        """创建网络状态标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        # 网络状态概览
        section = SectionCard("网络状态")
        
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(15)
        
        # 连接状态
        self.status_card = StatCard(
            title="连接状态",
            value="检查中...",
            icon="📶",
            color=COLORS["blue_main"]
        )
        grid_layout.addWidget(self.status_card)
        
        # IP地址
        self.ip_card = StatCard(
            title="IP地址",
            value="-",
            icon="🔌",
            color=COLORS["success"]
        )
        grid_layout.addWidget(self.ip_card)
        
        # 网关
        self.gateway_card = StatCard(
            title="网关",
            value="-",
            icon="🏠",
            color=COLORS["warning"]
        )
        grid_layout.addWidget(self.gateway_card)
        
        section.add_layout(grid_layout)
        layout.addWidget(section)
        
        # 刷新按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 刷新状态")
        refresh_btn.clicked.connect(self.refresh_network_status)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.tab_widget.addTab(tab, "📊 网络状态")
        
        # 初始刷新
        self.refresh_network_status()
    
    def create_ping_tab(self):
        """创建Ping测试标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("Ping测试")
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.ping_input = QLineEdit()
        self.ping_input.setPlaceholderText("输入IP地址或域名")
        self.ping_input.setText("www.baidu.com")
        input_layout.addWidget(self.ping_input)
        
        self.ping_btn = QPushButton("开始Ping")
        self.ping_btn.clicked.connect(self.start_ping)
        input_layout.addWidget(self.ping_btn)
        
        section.add_layout(input_layout)
        
        # 结果显示
        self.ping_result = QTextEdit()
        self.ping_result.setReadOnly(True)
        self.ping_result.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }}
        """)
        section.add_widget(self.ping_result)
        
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "🔔 Ping测试")
    
    def create_info_tab(self):
        """创建网络信息标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("网络适配器信息")
        
        self.adapter_list = QListWidget()
        self.adapter_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
            }}
        """)
        section.add_widget(self.adapter_list)
        
        layout.addWidget(section)
        
        # 加载适配器信息
        self.load_adapter_info()
        
        self.tab_widget.addTab(tab, "📋 适配器信息")
    
    def refresh_network_status(self):
        """刷新网络状态"""
        try:
            # 检查网络连接
            try:
                socket.create_connection(("www.baidu.com", 80), timeout=3)
                self.status_card.set_value("已连接")
                self.status_card.value_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            except:
                self.status_card.set_value("未连接")
                self.status_card.value_label.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold;")
            
            # 获取IP地址
            hostname = socket.gethostname()
            try:
                ip_address = socket.gethostbyname(hostname)
                self.ip_card.set_value(ip_address)
            except:
                self.ip_card.set_value("未知")
            
            # 获取网关
            try:
                result = subprocess.check_output(
                    ["ipconfig"],
                    text=True
                )
                lines = result.split("\n")
                for line in lines:
                    if "Default Gateway" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            gateway = parts[1].strip()
                            if gateway:
                                self.gateway_card.set_value(gateway)
                            break
            except:
                self.gateway_card.set_value("未知")
                
        except Exception as e:
            QMessageBox.warning(self, "警告", f"获取网络状态失败: {str(e)}")
    
    def start_ping(self):
        """开始Ping测试"""
        host = self.ping_input.text().strip()
        if not host:
            QMessageBox.warning(self, "警告", "请输入目标地址")
            return
        
        self.ping_result.clear()
        self.ping_btn.setEnabled(False)
        
        self.ping_thread = PingThread(host)
        self.ping_thread.result.connect(self.update_ping_result)
        self.ping_thread.finished.connect(lambda: setattr(self.ping_btn, 'setEnabled', True))
        self.ping_thread.start()
    
    def update_ping_result(self, result):
        """更新Ping结果"""
        self.ping_result.append(result)
    
    def load_adapter_info(self):
        """加载网络适配器信息"""
        self.adapter_list.clear()
        try:
            result = subprocess.check_output(
                ["ipconfig", "/all"],
                text=True
            )
            
            lines = result.split("\n")
            current_adapter = ""
            
            for line in lines:
                if "adapter" in line.lower() and ":" in line:
                    current_adapter = line.split(":")[0].strip()
                elif current_adapter and ("IPv4" in line or "IPv6" in line or "Physical" in line):
                    list_item = QListWidgetItem(f"{current_adapter}: {line.strip()}")
                    self.adapter_list.addItem(list_item)
                    
        except Exception as e:
            self.adapter_list.addItem(f"获取适配器信息失败: {str(e)}")