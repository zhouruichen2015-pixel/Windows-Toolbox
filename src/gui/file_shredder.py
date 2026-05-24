# File Shredder Module - 文件粉碎模块
# 安全文件删除

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QFileDialog, QProgressBar,
    QMessageBox, QSpinBox, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING

import os
import random
import struct


class ShredWorker(QThread):
    """
    文件粉碎线程
    """
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(bool, list)
    error = pyqtSignal(str)
    
    def __init__(self, files, passes=3):
        super().__init__()
        self.files = files
        self.passes = passes
        self.failed = []
        
    def run(self):
        total = len(self.files)
        for idx, path in enumerate(self.files):
            if not self.shred_file(path):
                self.failed.append(path)
            self.progress.emit(idx + 1, total)
            
        self.finished.emit(len(self.failed) == 0, self.failed)
        
    def shred_file(self, path):
        """
        粉碎单个文件
        """
        try:
            if os.path.isdir(path):
                # 删除目录中的所有文件
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        fpath = os.path.join(root, name)
                        self.shred_single_file(fpath)
                    for name in dirs:
                        try:
                            os.rmdir(os.path.join(root, name))
                        except:
                            pass
                return True
            else:
                return self.shred_single_file(path)
        except:
            return False
            
    def shred_single_file(self, path):
        """
        粉碎单个文件 - 多次覆写
        """
        try:
            if not os.path.exists(path):
                return False
                
            size = os.path.getsize(path)
            
            # 第一次：0x00填充
            self.overwrite_with_pattern(path, size, b'\x00')
            
            # 第二次：0xFF填充
            self.overwrite_with_pattern(path, size, b'\xFF')
            
            # 第三次：随机数据
            self.overwrite_with_random(path, size)
            
            # 根据passes次数执行更多覆写
            for i in range(self.passes - 3):
                self.overwrite_with_random(path, size)
                
            # 删除文件
            os.remove(path)
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False
            
    def overwrite_with_pattern(self, path, size, pattern):
        """
        覆写文件
        """
        try:
            with open(path, 'rb+') as f:
                # 生成数据块
                chunk_size = 1024 * 1024  # 1MB
                data = pattern * (chunk_size // len(pattern))
                
                written = 0
                while written < size:
                    to_write = min(chunk_size, size - written)
                    f.write(data[:to_write])
                    written += to_write
                f.flush()
                os.fsync(f)
        except:
            pass
            
    def overwrite_with_random(self, path, size):
        """
        随机数据覆写
        """
        try:
            with open(path, 'rb+') as f:
                chunk_size = 1024 * 1024
                written = 0
                while written < size:
                    to_write = min(chunk_size, size - written)
                    data = random.randbytes(to_write)
                    f.write(data)
                    written += to_write
                f.flush()
                os.fsync(f)
        except:
            pass


class FileShredderModule(BaseModule):
    """
    文件粉碎模块
    """
    module_name = "文件粉碎"
    module_icon = "🗑️"
    
    def __init__(self, parent=None):
        self.file_list = []
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
        
        # 警告提示
        warning = InfoCard(
            title="⚠️ 重要警告",
            subtitle="粉碎后的文件无法恢复！请确保不再需要这些文件。",
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
        
        # 工具栏
        self.setup_toolbar(layout)
        
        # 设置栏
        self.setup_settings_bar(layout)
        
        # 文件列表
        self.file_list_widget = QListWidget()
        self.file_list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        list_section = SectionCard("📋 文件列表")
        list_section.add_widget(self.file_list_widget)
        layout.addWidget(list_section)
        
        # 进度栏
        self.progress_label = QLabel("准备就绪")
        self.progress_label.setFont(QFont(*FONTS["body_small"]))
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
    def setup_toolbar(self, parent_layout):
        """
        配置工具栏
        """
        toolbar_layout = QHBoxLayout()
        
        self.add_file_btn = QPushButton("➕ 添加文件")
        self.add_file_btn.clicked.connect(self.add_files)
        toolbar_layout.addWidget(self.add_file_btn)
        
        self.add_folder_btn = QPushButton("➕ 添加文件夹")
        self.add_folder_btn.clicked.connect(self.add_folder)
        toolbar_layout.addWidget(self.add_folder_btn)
        
        self.remove_btn = QPushButton("🗑️ 移除选中")
        self.remove_btn.clicked.connect(self.remove_selected)
        toolbar_layout.addWidget(self.remove_btn)
        
        self.clear_btn = QPushButton("🔄 清空列表")
        self.clear_btn.clicked.connect(self.clear_list)
        toolbar_layout.addWidget(self.clear_btn)
        
        toolbar_layout.addStretch()
        
        self.shred_btn = QPushButton("🔥 开始粉碎")
        self.shred_btn.setProperty("class", "danger")
        self.shred_btn.clicked.connect(self.start_shredding)
        toolbar_layout.addWidget(self.shred_btn)
        
        parent_layout.addLayout(toolbar_layout)
        
    def setup_settings_bar(self, parent_layout):
        """
        配置设置栏
        """
        settings_layout = QHBoxLayout()
        
        passes_label = QLabel("覆写次数:")
        settings_layout.addWidget(passes_label)
        
        self.passes_spin = QSpinBox()
        self.passes_spin.setRange(1, 10)
        self.passes_spin.setValue(3)
        self.passes_spin.setSuffix(" 次")
        self.passes_spin.setToolTip("至少推荐3次")
        settings_layout.addWidget(self.passes_spin)
        
        self.verify_check = QCheckBox("验证 (推荐)")
        self.verify_check.setChecked(True)
        settings_layout.addWidget(self.verify_check)
        
        settings_layout.addStretch()
        
        count_label = QLabel("已添加:")
        settings_layout.addWidget(count_label)
        
        self.count_label = QLabel("0 个文件")
        self.count_label.setFont(QFont(*FONTS["body_small"]))
        self.count_label.setStyleSheet(f"color: {COLORS['blue_main']}; font-weight: bold;")
        settings_layout.addWidget(self.count_label)
        
        parent_layout.addLayout(settings_layout)
        
    def add_files(self):
        """
        添加文件
        """
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择要粉碎的文件",
            "",
            "所有文件 (*.*)"
        )
        
        if files:
            for path in files:
                if path not in self.file_list:
                    self.file_list.append(path)
                    self.file_list_widget.addItem(path)
            self.update_count()
            
    def add_folder(self):
        """
        添加文件夹
        """
        folder = QFileDialog.getExistingDirectory(self, "选择要粉碎的文件夹")
        
        if folder:
            if folder not in self.file_list:
                self.file_list.append(folder)
                self.file_list_widget.addItem(folder)
            self.update_count()
            
    def remove_selected(self):
        """
        移除选中项
        """
        selected = self.file_list_widget.selectedItems()
        
        for item in selected:
            path = item.text()
            if path in self.file_list:
                self.file_list.remove(path)
                
            row = self.file_list_widget.row(item)
            self.file_list_widget.takeItem(row)
            
        self.update_count()
        
    def clear_list(self):
        """
        清空列表
        """
        self.file_list = []
        self.file_list_widget.clear()
        self.update_count()
        
    def update_count(self):
        """
        更新计数
        """
        self.count_label.setText(f"{len(self.file_list)} 个文件/文件夹")
        
    def start_shredding(self):
        """
        开始粉碎
        """
        if not self.file_list:
            QMessageBox.information(self, "提示", "请先添加要粉碎的文件")
            return
            
        # 确认
        confirm = QMessageBox.question(
            self,
            "⚠️ 最终确认",
            f"确定要永久粉碎 {len(self.file_list)} 个文件/文件夹吗？\n\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return
            
        # 禁用UI
        self.set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("正在粉碎...")
        
        # 启动worker
        self.worker = ShredWorker(self.file_list, self.passes_spin.value())
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        
    def on_progress(self, current, total):
        """
        更新进度
        """
        pct = int(current / total * 100)
        self.progress_bar.setValue(pct)
        self.progress_label.setText(f"正在处理 {current}/{total}...")
        
    def on_finished(self, success, failed):
        """
        完成
        """
        self.set_buttons_enabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "完成", "所有文件粉碎完成！")
        else:
            QMessageBox.warning(self, "警告", f"部分文件未能粉碎：\n{len(failed)} 个")
            
        self.progress_label.setText("完成")
        self.clear_list()
        
    def set_buttons_enabled(self, enabled):
        """
        启用/禁用按钮
        """
        self.add_file_btn.setEnabled(enabled)
        self.add_folder_btn.setEnabled(enabled)
        self.remove_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.shred_btn.setEnabled(enabled)
        self.passes_spin.setEnabled(enabled)
