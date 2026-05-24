# System Optimizer Module - 系统优化模块
# 提供系统性能优化工具

import os
import subprocess
import shutil
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QTabWidget, QProgressBar,
    QScrollArea, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
from .card_widget import SectionCard, StatCard


class CleanThread(QThread):
    """清理线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, clean_types):
        super().__init__()
        self.clean_types = clean_types
    
    def run(self):
        try:
            total = len(self.clean_types)
            current = 0
            
            if "temp" in self.clean_types:
                current += 1
                self.progress_updated.emit(int(current/total*100), "清理临时文件...")
                self.clean_temp_files()
            
            if "cache" in self.clean_types:
                current += 1
                self.progress_updated.emit(int(current/total*100), "清理缓存文件...")
                self.clean_cache_files()
            
            if "recycle" in self.clean_types:
                current += 1
                self.progress_updated.emit(int(current/total*100), "清空回收站...")
                self.empty_recycle_bin()
            
            self.progress_updated.emit(100, "清理完成")
            self.finished.emit(True, "系统清理完成！")
        except Exception as e:
            self.finished.emit(False, f"清理失败: {str(e)}")
    
    def clean_temp_files(self):
        temp_dirs = [
            os.path.join(os.environ.get('TEMP', ''), ''),
            os.path.join(os.environ.get('TMP', ''), ''),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                    except:
                        pass
    
    def clean_cache_files(self):
        cache_dirs = [
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
        ]
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                for item in os.listdir(cache_dir):
                    item_path = os.path.join(cache_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                    except:
                        pass
    
    def empty_recycle_bin(self):
        try:
            subprocess.run(
                ["powershell", "-Command", "Clear-RecycleBin -Force"],
                check=True
            )
        except:
            pass


class SystemOptimizerModule(BaseModule):
    """系统优化模块 - 提供系统性能优化工具"""
    
    module_name = "系统优化"
    module_icon = "⚡"
    
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
        
        # 清理维护
        self.create_cleanup_tab()
        
        # 启动项管理
        self.create_startup_tab()
        
        # 服务管理
        self.create_services_tab()
    
    def create_cleanup_tab(self):
        """创建清理维护标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        # 清理选项
        section = SectionCard("清理选项")
        options_layout = QVBoxLayout()
        
        self.temp_check = QCheckBox("清理临时文件")
        self.temp_check.setChecked(True)
        options_layout.addWidget(self.temp_check)
        
        self.cache_check = QCheckBox("清理浏览器缓存")
        self.cache_check.setChecked(True)
        options_layout.addWidget(self.cache_check)
        
        self.recycle_check = QCheckBox("清空回收站")
        self.recycle_check.setChecked(False)
        options_layout.addWidget(self.recycle_check)
        
        section.add_layout(options_layout)
        layout.addWidget(section)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
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
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setFont(QFont(*FONTS["body_small"]))
        layout.addWidget(self.status_label)
        
        # 清理按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clean_button = QPushButton("开始清理")
        self.clean_button.clicked.connect(self.start_cleanup)
        button_layout.addWidget(self.clean_button)
        
        layout.addLayout(button_layout)
        
        self.tab_widget.addTab(tab, "🧹 系统清理")
    
    def create_startup_tab(self):
        """创建启动项管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("启动项管理")
        
        # 启动项列表
        self.startup_list = QListWidget()
        self.startup_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
            }}
        """)
        section.add_widget(self.startup_list)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.load_startup_items)
        button_layout.addWidget(refresh_btn)
        
        disable_btn = QPushButton("❌ 禁用")
        disable_btn.clicked.connect(self.disable_startup_item)
        button_layout.addWidget(disable_btn)
        
        section.add_layout(button_layout)
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "🚀 启动项管理")
        
        # 加载启动项
        self.load_startup_items()
    
    def create_services_tab(self):
        """创建服务管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(SPACING["card"])
        
        section = SectionCard("服务管理")
        
        # 服务列表
        self.services_list = QListWidget()
        self.services_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_border']};
                border-radius: {SPACING['input_radius']}px;
            }}
        """)
        section.add_widget(self.services_list)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.load_services)
        button_layout.addWidget(refresh_btn)
        
        start_btn = QPushButton("▶️ 启动")
        start_btn.clicked.connect(self.start_service)
        button_layout.addWidget(start_btn)
        
        stop_btn = QPushButton("⏹️ 停止")
        stop_btn.clicked.connect(self.stop_service)
        button_layout.addWidget(stop_btn)
        
        section.add_layout(button_layout)
        layout.addWidget(section)
        
        self.tab_widget.addTab(tab, "⚙️ 服务管理")
        
        # 加载服务
        self.load_services()
    
    def start_cleanup(self):
        """开始系统清理"""
        clean_types = []
        if self.temp_check.isChecked():
            clean_types.append("temp")
        if self.cache_check.isChecked():
            clean_types.append("cache")
        if self.recycle_check.isChecked():
            clean_types.append("recycle")
        
        if not clean_types:
            QMessageBox.warning(self, "警告", "请至少选择一项清理内容")
            return
        
        self.clean_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.clean_thread = CleanThread(clean_types)
        self.clean_thread.progress_updated.connect(self.update_progress)
        self.clean_thread.finished.connect(self.cleanup_finished)
        self.clean_thread.start()
    
    def update_progress(self, value, status):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(status)
    
    def cleanup_finished(self, success, message):
        """清理完成"""
        self.clean_button.setEnabled(True)
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.error(self, "错误", message)
    
    def load_startup_items(self):
        """加载启动项"""
        self.startup_list.clear()
        try:
            try:
                result = subprocess.check_output(
                    ["wmic", "startup", "get", "name,command"],
                    text=True
                )
                lines = result.strip().split('\n')[1:]  # 跳过标题行
                for line in lines:
                    if line.strip():
                        self.startup_list.addItem(line.strip())
            except Exception:
                try:
                    result = subprocess.check_output(
                        ["powershell", "-Command", 
                         "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run,HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run,HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run | Format-Table -AutoSize"],
                        text=True
                    )
                    lines = result.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            self.startup_list.addItem(line.strip())
                except Exception as e2:
                    self.startup_list.addItem("请使用任务管理器查看启动项\n提示: 部分功能需要管理员权限")
        except Exception as e:
            self.startup_list.addItem(f"获取启动项失败: {str(e)}")
    
    def disable_startup_item(self):
        """禁用启动项"""
        selected = self.startup_list.currentItem()
        if selected:
            QMessageBox.information(self, "提示", "启动项管理需要管理员权限，建议使用任务管理器进行管理")
    
    def load_services(self):
        """加载服务列表"""
        self.services_list.clear()
        try:
            try:
                result = subprocess.check_output(
                    ["wmic", "service", "get", "name,displayname,state"],
                    text=True
                )
                lines = result.strip().split('\n')[1:]  # 跳过标题行
                for line in lines[:50]:  # 只显示前50个
                    if line.strip():
                        parts = [p.strip() for p in line.split('  ') if p.strip()]
                        if len(parts) >= 3:
                            name = parts[0]
                            display_name = ' '.join(parts[1:-1])
                            status = parts[-1]
                            status_icon = "🟢" if status == 'Running' else "🔴"
                            list_item = QListWidgetItem(f"{status_icon} {display_name} ({status})")
                            list_item.setData(Qt.UserRole, name)
                            self.services_list.addItem(list_item)
            except Exception:
                try:
                    result = subprocess.check_output(
                        ["sc", "query"],
                        text=True
                    )
                    lines = result.strip().split('\n')
                    current_name = ""
                    current_display = ""
                    current_status = ""
                    count = 0
                    for line in lines:
                        if "SERVICE_NAME" in line:
                            if current_name and count < 50:
                                status_icon = "🟢" if "RUNNING" in current_status else "🔴"
                                list_item = QListWidgetItem(f"{status_icon} {current_display or current_name} ({current_status})")
                                list_item.setData(Qt.UserRole, current_name)
                                self.services_list.addItem(list_item)
                                count += 1
                            current_name = line.split(':')[1].strip()
                        elif "DISPLAY_NAME" in line:
                            current_display = line.split(':')[1].strip()
                        elif "STATE" in line:
                            current_status = line.split(':')[1].strip()
                    if current_name and count < 50:
                        status_icon = "🟢" if "RUNNING" in current_status else "🔴"
                        list_item = QListWidgetItem(f"{status_icon} {current_display or current_name} ({current_status})")
                        list_item.setData(Qt.UserRole, current_name)
                        self.services_list.addItem(list_item)
                except Exception as e2:
                    self.services_list.addItem("请使用服务管理工具(services.msc)查看\n提示: 部分功能需要管理员权限")
        except Exception as e:
            self.services_list.addItem(f"获取服务列表失败: {str(e)}")
    
    def start_service(self):
        """启动服务"""
        selected = self.services_list.currentItem()
        if selected:
            service_name = selected.data(Qt.UserRole)
            QMessageBox.information(self, "提示", f"启动服务需要管理员权限\n服务名: {service_name}")
    
    def stop_service(self):
        """停止服务"""
        selected = self.services_list.currentItem()
        if selected:
            service_name = selected.data(Qt.UserRole)
            QMessageBox.warning(self, "警告", f"停止服务需要管理员权限，请谨慎操作\n服务名: {service_name}")