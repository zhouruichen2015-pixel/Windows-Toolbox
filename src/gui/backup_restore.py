# Backup Restore Module - 备份恢复模块
# 提供数据备份和恢复功能

import os
import shutil
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QListWidget, QListWidgetItem, QLineEdit,
    QMessageBox, QFileDialog, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
from .card_widget import SectionCard, StatCard


class BackupThread(QThread):
    """备份线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, source, destination):
        super().__init__()
        self.source = source
        self.destination = destination
    
    def run(self):
        try:
            self.progress_updated.emit(0, "开始备份...")
            
            # 创建备份目录
            backup_dir = os.path.join(
                self.destination,
                f"Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            os.makedirs(backup_dir, exist_ok=True)
            
            # 复制文件
            self.progress_updated.emit(20, "复制文件中...")
            
            if os.path.isfile(self.source):
                shutil.copy2(self.source, backup_dir)
            elif os.path.isdir(self.source):
                shutil.copytree(self.source, os.path.join(backup_dir, os.path.basename(self.source)))
            
            self.progress_updated.emit(100, "备份完成")
            self.finished.emit(True, f"备份成功！\n备份位置: {backup_dir}")
        except Exception as e:
            self.finished.emit(False, f"备份失败: {str(e)}")


class BackupRestoreModule(BaseModule):
    """备份恢复模块 - 提供数据备份和恢复功能"""
    
    module_name = "备份恢复"
    module_icon = "📦"
    
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
        
        # 文件备份
        self.create_file_backup_tab()
        
        # 系统还原点
        self.create_restore_point_tab()
    
    def create_file_backup_tab(self):
        """创建文件备份标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("文件备份")
        
        # 源文件选择
        source_layout = QHBoxLayout()
        source_layout.setSpacing(10)
        
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("选择要备份的文件或文件夹")
        source_layout.addWidget(self.source_input)
        
        source_btn = QPushButton("浏览...")
        source_btn.clicked.connect(self.select_source)
        source_layout.addWidget(source_btn)
        
        section.add_layout(source_layout)
        
        # 目标位置选择
        dest_layout = QHBoxLayout()
        dest_layout.setSpacing(10)
        
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("选择备份目标位置")
        dest_layout.addWidget(self.dest_input)
        
        dest_btn = QPushButton("浏览...")
        dest_btn.clicked.connect(self.select_destination)
        dest_layout.addWidget(dest_btn)
        
        section.add_layout(dest_layout)
        
        # 进度条
        self.backup_progress = QProgressBar()
        self.backup_progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['gray_border']};
                border-radius: 10px;
                text-align: center;
                color: {COLORS['white']};
                font-weight: bold;
                height: 30px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['blue_main']};
                border-radius: 10px;
            }}
        """)
        section.add_widget(self.backup_progress)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.backup_btn = QPushButton("开始备份")
        self.backup_btn.clicked.connect(self.start_backup)
        button_layout.addWidget(self.backup_btn)
        
        section.add_layout(button_layout)
        
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "📁 文件备份")
    
    def create_restore_point_tab(self):
        """创建系统还原点标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("系统还原点")
        
        # 还原点列表
        self.restore_point_list = QListWidget()
        self.restore_point_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
            }}
        """)
        section.add_widget(self.restore_point_list)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        create_btn = QPushButton("➕ 创建还原点")
        create_btn.clicked.connect(self.create_restore_point)
        button_layout.addWidget(create_btn)
        
        refresh_btn = QPushButton("🔄 刷新列表")
        refresh_btn.clicked.connect(self.load_restore_points)
        button_layout.addWidget(refresh_btn)
        
        section.add_layout(button_layout)
        
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "🔄 系统还原")
        
        # 加载还原点列表
        self.load_restore_points()
    
    def select_source(self):
        """选择源文件/文件夹"""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFileOrDirectory)
        if dialog.exec_():
            self.source_input.setText(dialog.selectedFiles()[0])
    
    def select_destination(self):
        """选择目标位置"""
        path = QFileDialog.getExistingDirectory(self, "选择备份目录")
        if path:
            self.dest_input.setText(path)
    
    def start_backup(self):
        """开始备份"""
        source = self.source_input.text().strip()
        destination = self.dest_input.text().strip()
        
        if not source:
            QMessageBox.warning(self, "警告", "请选择要备份的文件或文件夹")
            return
        
        if not destination:
            QMessageBox.warning(self, "警告", "请选择备份目标位置")
            return
        
        if not os.path.exists(source):
            QMessageBox.warning(self, "警告", "源文件或文件夹不存在")
            return
        
        self.backup_btn.setEnabled(False)
        self.backup_progress.setValue(0)
        
        self.backup_thread = BackupThread(source, destination)
        self.backup_thread.progress_updated.connect(self.update_backup_progress)
        self.backup_thread.finished.connect(self.backup_finished)
        self.backup_thread.start()
    
    def update_backup_progress(self, value, status):
        """更新备份进度"""
        self.backup_progress.setValue(value)
    
    def backup_finished(self, success, message):
        """备份完成"""
        self.backup_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.error(self, "错误", message)
    
    def load_restore_points(self):
        """加载系统还原点列表"""
        self.restore_point_list.clear()
        try:
            try:
                result = subprocess.check_output(
                    ["wmic", "shadowcopy", "list", "brief"],
                    text=True
                )
                lines = result.strip().split('\n')[1:]  # 跳过标题行
                for line in lines[:20]:  # 只显示前20个
                    if line.strip():
                        self.restore_point_list.addItem(line.strip())
            except Exception:
                try:
                    result = subprocess.check_output(
                        ["powershell", "-Command", 
                         "Get-ComputerRestorePoint | Select-Object -First 10 Description, CreationTime | Format-Table -AutoSize"],
                        text=True
                    )
                    lines = result.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            self.restore_point_list.addItem(line.strip())
                except Exception as e2:
                    self.restore_point_list.addItem("请使用系统还原功能查看还原点\n提示: 需要管理员权限")
        except Exception as e:
            self.restore_point_list.addItem(f"获取还原点失败: {str(e)}")
    
    def create_restore_point(self):
        """创建系统还原点"""
        QMessageBox.information(self, "提示", "创建系统还原点需要管理员权限\n请在系统保护设置中手动创建还原点")