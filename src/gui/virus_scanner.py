# Virus Scanner Module - 病毒查杀模块
# 系统安全扫描

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QFileDialog, QProgressBar,
    QMessageBox, QTabWidget, QCheckBox, QGroupBox,
    QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING

import os
import hashlib
import time
from datetime import datetime


# 简单的"特征库"
SIGNATURES = {
    "test_malware": "this is a fake virus test file",
    "eicar": "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR",
}

DANGER_EXTENSIONS = [
    ".bat", ".cmd", ".exe", ".scr", ".pif", 
    ".reg", ".com", ".vbs", ".js", ".ps1"
]


class ScannerWorker(QThread):
    """
    扫描工作线程
    """
    progress = pyqtSignal(int, int)
    found = pyqtSignal(dict)
    finished = pyqtSignal(list)
    log = pyqtSignal(str)
    
    def __init__(self, scan_path, mode="quick"):
        super().__init__()
        self.scan_path = scan_path
        self.mode = mode
        self.threats = []
        
    def run(self):
        scanned = 0
        total = 0
        
        # 估算总文件数
        self.log.emit("正在计算扫描范围...")
        if self.mode == "quick":
            paths = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Downloads"),
                os.path.expanduser("~\\AppData\\Local\\Temp")
            ]
        elif self.mode == "full":
            paths = [os.path.abspath(os.sep)]
        else:
            paths = [self.scan_path]
            
        # 先数文件
        for path in paths:
            if not os.path.exists(path):
                continue
                
            if os.path.isfile(path):
                total += 1
            else:
                for root, dirs, files in os.walk(path):
                    total += len(files)
                    
        self.log.emit(f"准备扫描 {total} 个文件...")
        self.threats = []
        
        for scan_root in paths:
            if not os.path.exists(scan_root):
                continue
                
            if os.path.isfile(scan_root):
                self.scan_file(scan_root)
                scanned += 1
                self.progress.emit(scanned, total)
            else:
                for root, dirs, files in os.walk(scan_root):
                    for file in files:
                        full_path = os.path.join(root, file)
                        self.scan_file(full_path)
                        scanned += 1
                        if scanned % 100 == 0:
                            self.progress.emit(scanned, total)
                            
        self.finished.emit(self.threats)
        
    def scan_file(self, path):
        """
        扫描单个文件
        """
        try:
            # 1. 扩展名检查
            ext = os.path.splitext(path)[1].lower()
            if ext in DANGER_EXTENSIONS:
                self.threats.append({
                    "path": path,
                    "severity": "medium",
                    "type": "可疑扩展名",
                    "description": f"{ext} 扩展名是潜在危险的"
                })
                self.found.emit(self.threats[-1])
                
            # 2. 特征检查
            size = os.path.getsize(path)
            
            if size > 1024 * 1024:  # 大于1MB跳过详细检查
                return
                
            with open(path, 'rb') as f:
                content = f.read(4096)
                
                # 哈希检查
                file_hash = hashlib.sha256(content).hexdigest()
                
                # 简单字符串搜索
                content_str = content.decode('utf-8', errors='ignore')
                
                for sig_name, sig in SIGNATURES.items():
                    if sig in content_str:
                        self.threats.append({
                            "path": path,
                            "severity": "high",
                            "type": f"发现特征: {sig_name}",
                            "description": "文件包含已知威胁特征"
                        })
                        self.found.emit(self.threats[-1])
                        
        except:
            pass


class VirusScannerModule(BaseModule):
    """
    病毒查杀模块
    """
    module_name = "病毒查杀"
    module_icon = "🦠"
    
    def __init__(self, parent=None):
        self.worker = None
        self.quarantine = []
        super().__init__(parent)
        
    def setup_ui(self):
        """
        设置模块UI
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        layout.setSpacing(SPACING["card"])
        
        # 标题
        title_label = QLabel(f"{self.module_icon} {self.module_name}")
        title_label.setFont(QFont(*FONTS["title_large"]))
        title_label.setStyleSheet(f"color: {COLORS['blue_dark']};")
        layout.addWidget(title_label)
        
        # 信息卡片
        info = InfoCard(
            title="ℹ️  注意",
            subtitle="这是演示级扫描器。真实防护请使用专业杀毒软件。",
            icon="📌"
        )
        layout.addWidget(info)
        
        # 选项卡
        self.tabs = QTabWidget()
        
        # 扫描选项卡
        scan_tab = self.create_scan_tab()
        self.tabs.addTab(scan_tab, "🔍 扫描")
        
        # 隔离区选项卡
        quarantine_tab = self.create_quarantine_tab()
        self.tabs.addTab(quarantine_tab, "🛡️ 隔离区")
        
        layout.addWidget(self.tabs)
        
    def create_scan_tab(self):
        """
        创建扫描页
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 扫描模式选择
        mode_group = QGroupBox("📋 扫描模式")
        mode_layout = QVBoxLayout()
        
        self.scan_radio_quick = QRadioButton("⚡ 快速扫描 (桌面/下载/临时文件)")
        self.scan_radio_quick.setChecked(True)
        mode_layout.addWidget(self.scan_radio_quick)
        
        self.scan_radio_full = QRadioButton("🌐 全盘扫描 (较慢)")
        mode_layout.addWidget(self.scan_radio_full)
        
        self.scan_radio_custom = QRadioButton("📁 自定义路径...")
        mode_layout.addWidget(self.scan_radio_custom)
        
        self.custom_path_label = QLabel("未选择路径")
        self.custom_path_label.setFont(QFont(*FONTS["body_small"]))
        self.custom_path_label.setStyleSheet(f"color: {COLORS['gray_medium']};")
        
        self.select_path_btn = QPushButton("🔍 浏览...")
        self.select_path_btn.clicked.connect(self.select_custom_path)
        
        mode_layout.addWidget(self.custom_path_label)
        mode_layout.addWidget(self.select_path_btn)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # 扫描按钮
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ 开始扫描")
        self.start_btn.clicked.connect(self.start_scan)
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: {COLORS['white']};
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #388E3C;
            }}
        """)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ 停止")
        self.stop_btn.clicked.connect(self.stop_scan)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        layout.addLayout(btn_layout)
        
        # 进度
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("准备就绪")
        self.status_label.setFont(QFont(*FONTS["body_small"]))
        layout.addWidget(self.status_label)
        
        # 发现的威胁
        threat_group = QGroupBox("⚠️ 发现的威胁")
        threat_layout = QVBoxLayout()
        
        self.threat_list = QListWidget()
        threat_layout.addWidget(self.threat_list)
        
        threat_actions = QHBoxLayout()
        self.remove_btn = QPushButton("🗑️ 移除")
        self.remove_btn.clicked.connect(self.remove_selected)
        threat_actions.addWidget(self.remove_btn)
        
        self.quarantine_btn = QPushButton("🛡️ 隔离")
        self.quarantine_btn.clicked.connect(self.quarantine_selected)
        threat_actions.addWidget(self.quarantine_btn)
        
        threat_layout.addLayout(threat_actions)
        threat_group.setLayout(threat_layout)
        layout.addWidget(threat_group)
        
        return widget
        
    def create_quarantine_tab(self):
        """
        创建隔离区页
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.quarantine_list = QListWidget()
        layout.addWidget(self.quarantine_list)
        
        q_actions = QHBoxLayout()
        self.restore_btn = QPushButton("↩️ 恢复")
        self.restore_btn.clicked.connect(self.restore_selected)
        q_actions.addWidget(self.restore_btn)
        
        self.delete_btn = QPushButton("💀 永久删除")
        self.delete_btn.clicked.connect(self.delete_quarantine_selected)
        q_actions.addWidget(self.delete_btn)
        
        layout.addLayout(q_actions)
        
        return widget
        
    def select_custom_path(self):
        """
        选择自定义扫描路径
        """
        path = QFileDialog.getExistingDirectory(self, "选择扫描路径")
        if path:
            self.scan_radio_custom.setChecked(True)
            self.custom_path_label.setText(path)
            
    def start_scan(self):
        """
        开始扫描
        """
        mode = None
        path = None
        
        if self.scan_radio_quick.isChecked():
            mode = "quick"
        elif self.scan_radio_full.isChecked():
            mode = "full"
        else:
            path = self.custom_path_label.text()
            if path == "未选择路径":
                QMessageBox.information(self, "提示", "请先选择扫描路径")
                return
            mode = "custom"
            
        # 禁用UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 清空威胁列表
        self.threat_list.clear()
        
        # 启动worker
        self.worker = ScannerWorker(path or "", mode)
        self.worker.progress.connect(self.on_scan_progress)
        self.worker.found.connect(self.on_threat_found)
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.log.connect(self.status_label.setText)
        self.worker.start()
        
    def stop_scan(self):
        """
        停止扫描
        """
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker = None
            
        self.on_scan_finished([])
        
    def on_scan_progress(self, current, total):
        """
        更新进度
        """
        if total > 0:
            pct = int(current / total * 100)
            self.progress_bar.setValue(pct)
            self.status_label.setText(f"扫描中... {current}/{total}")
            
    def on_threat_found(self, threat):
        """
        发现威胁
        """
        color = COLORS['warning']
        if threat['severity'] == "high":
            color = COLORS['danger']
            
        item = QListWidgetItem(f"[{threat['severity']}] {threat['type']} - {os.path.basename(threat['path'])}")
        item.setData(Qt.UserRole, threat)
        item.setForeground(color)
        
        self.threat_list.addItem(item)
        
    def on_scan_finished(self, threats):
        """
        扫描完成
        """
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if len(threats) > 0:
            QMessageBox.information(self, "完成", f"扫描完成！发现 {len(threats)} 个威胁")
        else:
            QMessageBox.information(self, "完成", "扫描完成！系统安全！")
            
    def remove_selected(self):
        """
        移除选中威胁（从列表）
        """
        selected = self.threat_list.selectedItems()
        for item in selected:
            row = self.threat_list.row(item)
            self.threat_list.takeItem(row)
            
    def quarantine_selected(self):
        """
        隔离选中威胁
        """
        selected = self.threat_list.selectedItems()
        if not selected:
            QMessageBox.information(self, "提示", "请先选择威胁")
            return
            
        for item in selected:
            threat = item.data(Qt.UserRole)
            self.quarantine.append(threat)
            q_item = QListWidgetItem(f"[隔离] {os.path.basename(threat['path'])}")
            q_item.setData(Qt.UserRole, threat)
            self.quarantine_list.addItem(q_item)
            
            # 从威胁列表移除
            row = self.threat_list.row(item)
            self.threat_list.takeItem(row)
            
        QMessageBox.information(self, "成功", f"已隔离 {len(selected)} 项")
        
    def restore_selected(self):
        """
        恢复选中项
        """
        QMessageBox.information(self, "演示", "恢复功能在完整版本中可用")
        
    def delete_quarantine_selected(self):
        """
        永久删除
        """
        selected = self.quarantine_list.selectedItems()
        if not selected:
            return
            
        confirm = QMessageBox.question(
            self,
            "确认",
            f"确定要永久删除 {len(selected)} 项吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            for item in selected:
                row = self.quarantine_list.row(item)
                self.quarantine_list.takeItem(row)
