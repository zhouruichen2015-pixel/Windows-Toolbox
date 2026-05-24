# Task Manager Module - 任务管理器模块
# 进程管理和系统资源监控

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QPushButton, QLineEdit, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox,
    QTabWidget, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtGui import QFont, QColor, QBrush

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING

import psutil
import time
from datetime import datetime


class ProcessWorker(QThread):
    """
    进程数据采集线程
    """
    data_ready = pyqtSignal(list)
    perf_ready = pyqtSignal(dict)
    
    def run(self):
        while True:
            # 采集进程列表
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'create_time', 'status']):
                try:
                    with proc.oneshot():
                        mem_info = proc.memory_info()
                        processes.append({
                            "pid": proc.pid,
                            "name": proc.name(),
                            "cpu": proc.cpu_percent(),
                            "memory": mem_info.rss / (1024 * 1024),
                            "start_time": datetime.fromtimestamp(proc.create_time()).strftime("%H:%M:%S"),
                            "status": proc.status()
                        })
                except:
                    continue
            
            # 按CPU使用排序
            processes.sort(key=lambda x: x["cpu"], reverse=True)
            
            self.data_ready.emit(processes[:100])
            
            # 系统性能数据
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.perf_ready.emit({
                "cpu": cpu_percent,
                "memory": memory.percent,
                "memory_used": self.format_bytes(memory.used),
                "memory_total": self.format_bytes(memory.total),
                "disk": disk.percent
            })
            
    def format_bytes(self, bytes_val):
        for unit in ['MB', 'GB', 'TB']:
            if bytes_val < (1024 ** 2 if unit == 'MB' else 1024 ** 3 if unit == 'GB' else 1024 ** 4):
                return f"{bytes_val / (1024 ** 2):.1f} {unit}"
        return f"{bytes_val / (1024 ** 3):.1f} TB"


class ProcessFilterProxy(QSortFilterProxyModel):
    """
    进程搜索过滤代理
    """
    def __init__(self):
        super().__init__()
        self.filter_text = ""
        
    def setFilterText(self, text):
        self.filter_text = text.lower()
        self.invalidateFilter()


class TaskManagerModule(BaseModule):
    """
    任务管理器模块
    """
    module_name = "任务管理器"
    module_icon = "⚙️"
    
    def __init__(self, parent=None):
        self.process_list = []
        self.worker = None
        super().__init__(parent)
        
    def setup_ui(self):
        """
        设置模块UI
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        layout.setSpacing(SPACING["card"])
        
        # 标题 - 居中显示
        title_label = QLabel(f"{self.module_icon} {self.module_name}")
        title_label.setFont(QFont(*FONTS["title_large"]))
        title_label.setStyleSheet(f"color: {COLORS['blue_dark']};")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFixedHeight(40)
        layout.addWidget(title_label)
        
        # 顶部搜索和工具栏
        toolbar_widget = QWidget()
        toolbar_widget.setStyleSheet("background-color: #f5f5f5; border-radius: 8px; padding: 10px;")
        self.setup_toolbar(toolbar_widget)
        layout.addWidget(toolbar_widget)
        
        # 内容区 - 左侧进程表，右侧性能
        content_splitter = QSplitter(Qt.Horizontal)
        
        # 进程列表区
        process_section = SectionCard("📋 进程列表")
        self.setup_process_list(process_section)
        content_splitter.addWidget(process_section)
        
        # 性能监控区
        perf_section = SectionCard("📊 系统性能")
        self.setup_performance_chart(perf_section)
        content_splitter.addWidget(perf_section)
        
        content_splitter.setStretchFactor(0, 2)
        content_splitter.setStretchFactor(1, 1)
        
        layout.addWidget(content_splitter)
        
    def setup_toolbar(self, parent_widget):
        """
        配置工具栏
        """
        toolbar_layout = QHBoxLayout(parent_widget)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(15)
        
        search_label = QLabel("🔍 搜索:")
        search_label.setFont(QFont(*FONTS["body"]))
        toolbar_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索进程名称...")
        self.search_input.textChanged.connect(self.on_search)
        toolbar_layout.addWidget(self.search_input, 1)
        
        # 添加伸缩空间
        toolbar_layout.addStretch()
        
        self.end_task_btn = QPushButton("⛔ 结束进程")
        self.end_task_btn.clicked.connect(self.end_selected_process)
        toolbar_layout.addWidget(self.end_task_btn)
        
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.clicked.connect(self.force_refresh)
        toolbar_layout.addWidget(self.refresh_btn)
        
    def setup_process_list(self, parent_section):
        """
        配置进程列表
        """
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(6)
        self.process_table.setHorizontalHeaderLabels(["PID", "进程名", "CPU %", "内存 (MB)", "启动时间", "状态"])
        self.process_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.process_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # 设置表头样式
        header = self.process_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        
        parent_section.add_widget(self.process_table)
        
    def setup_performance_chart(self, parent_section):
        """
        配置性能监控区
        """
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # 状态显示标签
        self.cpu_label = QLabel("🖥️ CPU: 获取中...")
        self.cpu_label.setFont(QFont(*FONTS["body"]))
        self.cpu_label.setStyleSheet(f"background-color: {COLORS['white']}; padding: 15px; border-radius: 8px; border: 1px solid {COLORS['gray_border']};")
        grid.addWidget(self.cpu_label, 0, 0)
        
        self.memory_label = QLabel("🧠 内存: 获取中...")
        self.memory_label.setFont(QFont(*FONTS["body"]))
        self.memory_label.setStyleSheet(f"background-color: {COLORS['white']}; padding: 15px; border-radius: 8px; border: 1px solid {COLORS['gray_border']};")
        grid.addWidget(self.memory_label, 0, 1)
        
        self.disk_label = QLabel("💾 磁盘: 获取中...")
        self.disk_label.setFont(QFont(*FONTS["body"]))
        self.disk_label.setStyleSheet(f"background-color: {COLORS['white']}; padding: 15px; border-radius: 8px; border: 1px solid {COLORS['gray_border']};")
        grid.addWidget(self.disk_label, 1, 0, 1, 2)
        
        info_card = InfoCard(
            title="💡 提示",
            subtitle="双击进程可查看详情，选择后点击'结束进程'可终止",
            icon="📌"
        )
        grid.addWidget(info_card, 2, 0, 1, 2)
        
        parent_section.add_layout(grid)
        
    def on_module_enter(self):
        """
        模块激活时
        """
        self.start_monitoring()
        
    def on_module_leave(self):
        """
        模块离开时
        """
        self.stop_monitoring()
        
    def start_monitoring(self):
        """
        启动监控线程
        """
        if self.worker is None:
            self.worker = ProcessWorker()
            self.worker.data_ready.connect(self.on_process_data)
            self.worker.perf_ready.connect(self.on_perf_data)
            self.worker.start()
            
    def stop_monitoring(self):
        """
        停止监控线程
        """
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker = None
            
    def on_process_data(self, processes):
        """
        更新进程列表
        """
        self.process_list = processes
        
        # 应用搜索过滤
        search_text = self.search_input.text().lower()
        if search_text:
            filtered = [p for p in processes if search_text in p["name"].lower()]
            self.populate_table(filtered)
        else:
            self.populate_table(processes)
            
    def populate_table(self, processes):
        """
        填充进程表
        """
        self.process_table.setRowCount(len(processes))
        
        for row, proc in enumerate(processes):
            self.process_table.setItem(row, 0, QTableWidgetItem(str(proc["pid"])))
            self.process_table.setItem(row, 1, QTableWidgetItem(proc["name"]))
            
            cpu_item = QTableWidgetItem(f"{proc['cpu']:.1f}%")
            if proc['cpu'] > 80:
                cpu_item.setForeground(QBrush(QColor(COLORS['danger'])))
            elif proc['cpu'] > 50:
                cpu_item.setForeground(QBrush(QColor(COLORS['warning'])))
            self.process_table.setItem(row, 2, cpu_item)
            
            mem_item = QTableWidgetItem(f"{proc['memory']:.1f}")
            self.process_table.setItem(row, 3, mem_item)
            
            self.process_table.setItem(row, 4, QTableWidgetItem(proc["start_time"]))
            self.process_table.setItem(row, 5, QTableWidgetItem(proc["status"]))
            
    def on_perf_data(self, data):
        """
        更新性能数据
        """
        self.cpu_label.setText(f"🖥️ CPU: {data['cpu']}% 使用")
        self.memory_label.setText(f"🧠 内存: {data['memory']}% ({data['memory_used']} / {data['memory_total']})")
        self.disk_label.setText(f"💾 磁盘: {data['disk']}% 已用")
        
    def on_search(self):
        """
        搜索过滤
        """
        if self.process_list:
            self.on_process_data(self.process_list)
            
    def end_selected_process(self):
        """
        结束选中进程
        """
        selected_items = self.process_table.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "提示", "请先选择要结束的进程")
            return
            
        pid_item = self.process_table.item(selected_items[0].row(), 0)
        name_item = self.process_table.item(selected_items[0].row(), 1)
        
        try:
            pid = int(pid_item.text())
            confirm = QMessageBox.question(
                self,
                "确认",
                f"确定要终止进程 {name_item.text()} (PID: {pid}) 吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                proc = psutil.Process(pid)
                proc.terminate()
                QMessageBox.information(self, "成功", "进程已终止")
                self.force_refresh()
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法终止进程: {str(e)}")
            
    def force_refresh(self):
        """
        强制刷新（重新启动worker）
        """
        self.stop_monitoring()
        self.start_monitoring()
