# Security Scanner Module - 安全扫描模块
# 提供系统安全检测功能

import os
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QListWidget, QListWidgetItem, QProgressBar,
    QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
from .card_widget import SectionCard, StatCard


class ScanThread(QThread):
    """扫描线程"""
    progress_updated = pyqtSignal(int, str)
    result_found = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, scan_types):
        super().__init__()
        self.scan_types = scan_types
        self.results = []
    
    def run(self):
        try:
            total = len(self.scan_types)
            current = 0
            
            if "quick" in self.scan_types:
                current += 1
                self.progress_updated.emit(int(current/total*33), "快速扫描...")
                self.quick_scan()
            
            if "deep" in self.scan_types:
                current += 1
                self.progress_updated.emit(int(current/total*33 + 33), "深度扫描...")
                self.deep_scan()
            
            if "custom" in self.scan_types:
                current += 1
                self.progress_updated.emit(90, "自定义扫描...")
                self.custom_scan()
            
            self.progress_updated.emit(100, "扫描完成")
            
            if self.results:
                self.finished.emit(True, f"扫描完成！发现 {len(self.results)} 个安全项")
            else:
                self.finished.emit(True, "扫描完成！未发现安全问题")
        except Exception as e:
            self.finished.emit(False, f"扫描失败: {str(e)}")
    
    def quick_scan(self):
        """快速扫描"""
        temp_dir = os.environ.get('TEMP', '')
        if temp_dir:
            try:
                files = os.listdir(temp_dir)
                suspicious_extensions = ['.exe', '.bat', '.cmd', '.ps1']
                for f in files[:100]:
                    if any(f.endswith(ext) for ext in suspicious_extensions):
                        self.results.append(f"临时目录可疑文件: {f}")
            except:
                pass
    
    def deep_scan(self):
        """深度扫描"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled"],
                text=True
            )
            if "AntivirusEnabled" in result.stdout:
                if "False" in result.stdout:
                    self.results.append("⚠️ Windows Defender 已禁用")
        except:
            pass
    
    def custom_scan(self):
        """自定义扫描"""
        pass


class SecurityScannerModule(BaseModule):
    """安全扫描模块 - 提供系统安全检测功能"""
    
    module_name = "安全扫描"
    module_icon = "🛡️"
    
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
        
        # 安全扫描
        self.create_scan_tab()
        
        # 安全设置
        self.create_settings_tab()
    
    def create_scan_tab(self):
        """创建安全扫描标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        # 扫描选项
        section = SectionCard("扫描选项")
        
        options_layout = QVBoxLayout()
        
        self.quick_check = QCheckBox("快速扫描 - 扫描常见威胁区域")
        self.quick_check.setChecked(True)
        options_layout.addWidget(self.quick_check)
        
        self.deep_check = QCheckBox("深度扫描 - 全面系统检查")
        self.deep_check.setChecked(False)
        options_layout.addWidget(self.deep_check)
        
        self.custom_check = QCheckBox("自定义扫描")
        self.custom_check.setChecked(False)
        options_layout.addWidget(self.custom_check)
        
        section.add_layout(options_layout)
        layout.addWidget(section)
        
        # 进度条
        self.scan_progress = QProgressBar()
        self.scan_progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['gray_border']};
                border-radius: 10px;
                text-align: center;
                color: {COLORS['white']};
                font-weight: bold;
                height: 30px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['success']};
                border-radius: 10px;
            }}
        """)
        layout.addWidget(self.scan_progress)
        
        # 扫描结果
        self.scan_results = QListWidget()
        self.scan_results.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
            }}
        """)
        layout.addWidget(self.scan_results)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.scan_btn = QPushButton("🔍 开始扫描")
        self.scan_btn.clicked.connect(self.start_scan)
        button_layout.addWidget(self.scan_btn)
        
        clear_btn = QPushButton("🗑️ 清除结果")
        clear_btn.clicked.connect(self.clear_results)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        self.tab_widget.addTab(tab, "🔍 安全扫描")
    
    def create_settings_tab(self):
        """创建安全设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("安全建议")
        
        tips = [
            "🔒 定期更新操作系统和驱动程序",
            "🔐 使用强密码并定期更换",
            "🛡️ 保持杀毒软件实时保护开启",
            "⚠️ 谨慎下载和运行未知来源的文件",
            "💾 定期备份重要数据",
            "🔍 定期扫描系统以检测恶意软件"
        ]
        
        for tip in tips:
            tip_label = QLabel(tip)
            tip_label.setFont(QFont(*FONTS["body"]))
            section.add_widget(tip_label)
        
        layout.addWidget(section)
        
        # Windows安全中心
        section2 = SectionCard("系统安全工具")
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        defender_btn = QPushButton("🛡️ Windows安全中心")
        defender_btn.clicked.connect(self.open_defender)
        button_layout.addWidget(defender_btn)
        
        firewall_btn = QPushButton("🔥 Windows防火墙")
        firewall_btn.clicked.connect(self.open_firewall)
        button_layout.addWidget(firewall_btn)
        
        section2.add_layout(button_layout)
        layout.addWidget(section2)
        
        self.tab_widget.addTab(tab, "⚙️ 安全设置")
    
    def start_scan(self):
        """开始安全扫描"""
        scan_types = []
        if self.quick_check.isChecked():
            scan_types.append("quick")
        if self.deep_check.isChecked():
            scan_types.append("deep")
        if self.custom_check.isChecked():
            scan_types.append("custom")
        
        if not scan_types:
            QMessageBox.warning(self, "警告", "请至少选择一项扫描类型")
            return
        
        self.scan_results.clear()
        self.scan_btn.setEnabled(False)
        self.scan_progress.setValue(0)
        
        self.scan_thread = ScanThread(scan_types)
        self.scan_thread.progress_updated.connect(self.update_scan_progress)
        self.scan_thread.result_found.connect(self.add_scan_result)
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.start()
    
    def update_scan_progress(self, value, status):
        """更新扫描进度"""
        self.scan_progress.setValue(value)
    
    def add_scan_result(self, result):
        """添加扫描结果"""
        item = QListWidgetItem(result)
        self.scan_results.addItem(item)
    
    def scan_finished(self, success, message):
        """扫描完成"""
        self.scan_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "扫描完成", message)
        else:
            QMessageBox.error(self, "错误", message)
    
    def clear_results(self):
        """清除扫描结果"""
        self.scan_results.clear()
    
    def open_defender(self):
        """打开Windows安全中心"""
        try:
            subprocess.run(["ms-settings:windowsdefender"], check=True)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法打开Windows安全中心: {str(e)}")
    
    def open_firewall(self):
        """打开Windows防火墙"""
        try:
            subprocess.run(["wf.msc"], check=True)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法打开Windows防火墙: {str(e)}")