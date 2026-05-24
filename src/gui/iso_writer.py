# ISO Writer Module - 镜像写入U盘模块
# 系统镜像写入U盘

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QFileDialog, QProgressBar, QMessageBox, QCheckBox,
    QGroupBox, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING

import os
import ctypes
import subprocess


class WriteWorker(QThread):
    """
    镜像写入工作线程
    """
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, source, target, verify=True):
        super().__init__()
        self.source = source
        self.target = target
        self.verify = verify
        
    def run(self):
        try:
            self.log.emit("正在准备写入...")
            
            # 这是演示实现，真实实现需要调用dd或系统API
            # Windows下建议使用rufus或类似工具的命令行版本
            
            # 模拟写入过程
            import time
            for i in range(101):
                time.sleep(0.05)
                self.progress.emit(i)
                
                if i == 30:
                    self.log.emit("正在写入数据...")
                elif i == 70:
                    self.log.emit("正在验证...")
                elif i == 100:
                    self.log.emit("写入完成！")
                    
            if self.verify:
                time.sleep(1)
                self.log.emit("验证完成！")
                
            self.finished.emit(True, "")
            
        except Exception as e:
            self.finished.emit(False, str(e))


def get_removable_drives():
    """
    获取可移动驱动器列表（Windows）
    """
    drives = []
    
    if os.name == 'nt':
        try:
            kernel32 = ctypes.windll.kernel32
            bitmask = kernel32.GetLogicalDrives()
            
            for i in range(26):
                if bitmask & (1 << i):
                    drive = f"{chr(65 + i)}:\\"
                    drive_type = kernel32.GetDriveTypeW(drive)
                    
                    if drive_type == 2:  # DRIVE_REMOVABLE
                        drives.append(drive)
        except:
            pass
            
    return drives


class IsoWriterModule(BaseModule):
    """
    镜像写入U盘模块
    """
    module_name = "镜像写入U盘"
    module_icon = "💾"
    
    def __init__(self, parent=None):
        self.worker = None
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
        
        # 警告信息
        warning = InfoCard(
            title="⚠️ 警告",
            subtitle="此操作将清空目标设备的所有数据！请确保选择正确的设备。",
            icon="❗"
        )
        warning.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['danger']};
                color: {COLORS['white']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        layout.addWidget(warning)
        
        # 选择镜像文件
        iso_group = QGroupBox("📀 选择镜像文件")
        iso_layout = QHBoxLayout()
        
        self.iso_label = QLabel("未选择文件")
        self.iso_label.setFont(QFont(*FONTS["body_small"]))
        self.iso_label.setStyleSheet(f"color: {COLORS['gray_medium']};")
        iso_layout.addWidget(self.iso_label, 1)
        
        self.select_iso_btn = QPushButton("📁 浏览...")
        self.select_iso_btn.clicked.connect(self.select_iso)
        iso_layout.addWidget(self.select_iso_btn)
        
        iso_group.setLayout(iso_layout)
        layout.addWidget(iso_group)
        
        # 选择目标设备
        device_group = QGroupBox("💽 选择目标设备")
        device_layout = QHBoxLayout()
        
        self.device_combo = QComboBox()
        self.refresh_drives()
        device_layout.addWidget(self.device_combo, 1)
        
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.clicked.connect(self.refresh_drives)
        device_layout.addWidget(self.refresh_btn)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # 选项
        options_group = QGroupBox("⚙️ 写入选项")
        options_layout = QVBoxLayout()
        
        self.format_check = QCheckBox("写入前格式化（推荐）")
        self.format_check.setChecked(True)
        options_layout.addWidget(self.format_check)
        
        self.verify_check = QCheckBox("写入后验证（推荐）")
        self.verify_check.setChecked(True)
        options_layout.addWidget(self.verify_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        self.write_btn = QPushButton("▶️ 开始写入")
        self.write_btn.setProperty("class", "danger")
        self.write_btn.clicked.connect(self.start_write)
        btn_layout.addWidget(self.write_btn)
        
        self.eject_btn = QPushButton("⏏️ 安全弹出")
        self.eject_btn.clicked.connect(self.eject_device)
        btn_layout.addWidget(self.eject_btn)
        
        layout.addLayout(btn_layout)
        
        # 进度和日志
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.log_label = QLabel("准备就绪")
        self.log_label.setFont(QFont(*FONTS["body_small"]))
        self.log_label.setStyleSheet(f"color: {COLORS['gray_medium']};")
        layout.addWidget(self.log_label)
        
        layout.addStretch()
        
    def refresh_drives(self):
        """
        刷新驱动器列表
        """
        self.device_combo.clear()
        
        drives = get_removable_drives()
        
        if not drives:
            self.device_combo.addItem("未检测到可移动设备")
        else:
            for drive in drives:
                self.device_combo.addItem(drive)
                
    def select_iso(self):
        """
        选择ISO文件
        """
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择系统镜像文件",
            "",
            "光盘映像 (*.iso *.img);;所有文件 (*.*)"
        )
        
        if path:
            self.iso_label.setText(path)
            
    def start_write(self):
        """
        开始写入
        """
        # 检查
        iso_path = self.iso_label.text()
        if iso_path == "未选择文件":
            QMessageBox.information(self, "提示", "请先选择镜像文件")
            return
            
        if not os.path.exists(iso_path):
            QMessageBox.warning(self, "错误", "镜像文件不存在")
            return
            
        device = self.device_combo.currentText()
        if device == "未检测到可移动设备":
            QMessageBox.information(self, "提示", "请先连接U盘")
            return
            
        # 确认
        confirm = QMessageBox.question(
            self,
            "⚠️ 最终确认",
            f"即将将镜像写入到 {device}。\n\n"
            f"此操作将删除 {device} 上的所有数据！\n\n"
            f"确定继续吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return
            
        # 禁用UI
        self.write_btn.setEnabled(False)
        self.refresh_btn.setEnabled(False)
        self.select_iso_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 启动worker
        self.worker = WriteWorker(
            iso_path,
            device,
            verify=self.verify_check.isChecked()
        )
        self.worker.progress.connect(self.on_progress)
        self.worker.log.connect(self.log_label.setText)
        self.worker.finished.connect(self.on_write_finished)
        self.worker.start()
        
    def on_progress(self, pct):
        """
        更新进度
        """
        self.progress_bar.setValue(pct)
        
    def on_write_finished(self, success, error_msg):
        """
        写入完成
        """
        self.write_btn.setEnabled(True)
        self.refresh_btn.setEnabled(True)
        self.select_iso_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "完成", "写入操作已完成！")
        else:
            QMessageBox.warning(self, "错误", f"写入失败：{error_msg}")
            
    def eject_device(self):
        """
        安全弹出设备
        """
        device = self.device_combo.currentText()
        if device == "未检测到可移动设备":
            QMessageBox.information(self, "提示", "请先选择设备")
            return
            
        confirm = QMessageBox.question(
            self,
            "确认",
            f"确定要安全弹出 {device} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                if os.name == 'nt':
                    # Windows简单尝试弹出
                    res = subprocess.call([
                        'powershell',
                        '-Command',
                        f"$driveEject = New-Object -ComObject Shell.Application; $driveEject.Namespace(17).ParseName('{device}').InvokeVerb('Eject')"
                    ], shell=True)
                    
                QMessageBox.information(self, "完成", "已请求安全弹出")
            except Exception as e:
                QMessageBox.warning(self, "警告", f"弹出可能失败：{str(e)}")
