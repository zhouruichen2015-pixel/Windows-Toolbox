# System Monitor Module - 电脑配置数据大屏模块
# 显示硬件配置和性能数据

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QFrame
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING
from .gauge_widget import GaugeWidget

import os
import platform
import psutil
import json


class PerformanceWorker(QThread):
    """
    性能数据采集线程
    """
    data_ready = pyqtSignal(dict)
    
    def run(self):
        while True:
            # 采集性能数据
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            net = self.get_network_speed()
            
            self.data_ready.emit({
                "cpu": cpu_percent,
                "memory": memory.percent,
                "disk": disk.percent,
                "memory_used": self.format_bytes(memory.used),
                "memory_total": self.format_bytes(memory.total),
                "disk_used": self.format_bytes(disk.used),
                "disk_total": self.format_bytes(disk.total),
                "network": net
            })
            
    def format_bytes(self, bytes_val):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024
        return f"{bytes_val:.1f} PB"
        
    def get_network_speed(self):
        # 获取简单的网络统计
        net_io = psutil.net_io_counters()
        return f"{self.format_bytes(net_io.bytes_sent)}/s ↗ / {self.format_bytes(net_io.bytes_recv)}/s ↘"


class SystemMonitorModule(BaseModule):
    """
    电脑配置数据大屏模块
    """
    module_name = "电脑配置数据大屏"
    module_icon = "📊"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.timer = None
        
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
        
        # 上半部分 - 硬件信息卡片
        hardware_section = SectionCard("💻 硬件信息")
        self.setup_hardware_info(hardware_section)
        layout.addWidget(hardware_section)
        
        # 下半部分 - 性能监控
        perf_section = SectionCard("📈 实时性能")
        self.setup_performance_metrics(perf_section)
        layout.addWidget(perf_section)
        
        layout.addStretch()
        
    def setup_hardware_info(self, parent_section):
        """
        配置硬件信息展示区
        """
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # 获取系统信息
        system_info = self.get_system_info()
        
        # 1. CPU信息
        cpu_card = InfoCard(
            title=f"{system_info['cpu_name']}",
            subtitle=f"核心数: {system_info['cpu_cores']}",
            icon="🖥️"
        )
        grid.addWidget(cpu_card, 0, 0)
        
        # 2. 内存信息
        mem_card = InfoCard(
            title=f"{system_info['memory_total']} 内存",
            subtitle=f"可用: {system_info['memory_available']}",
            icon="🧠"
        )
        grid.addWidget(mem_card, 0, 1)
        
        # 3. 磁盘信息
        disk_card = InfoCard(
            title=f"{system_info['disk_total']} 存储空间",
            subtitle=f"可用: {system_info['disk_available']}",
            icon="💾"
        )
        grid.addWidget(disk_card, 0, 2)
        
        # 4. 系统信息
        system_card = InfoCard(
            title=system_info['os_name'],
            subtitle=f"{system_info['os_version']}",
            icon="🪟"
        )
        grid.addWidget(system_card, 1, 0)
        
        # 5. 主机名
        host_card = InfoCard(
            title=system_info['hostname'],
            subtitle=f"Python: {platform.python_version()}",
            icon="🏠"
        )
        grid.addWidget(host_card, 1, 1)
        
        # 6. 开机时间
        boot_card = InfoCard(
            title=f"运行: {self.get_uptime()}",
            subtitle=f"当前用户: {os.getenv('USERNAME', 'Unknown')}",
            icon="⏱️"
        )
        grid.addWidget(boot_card, 1, 2)
        
        parent_section.add_layout(grid)
        
    def setup_performance_metrics(self, parent_section):
        """
        配置性能监控区
        """
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # 仪表盘控件
        self.cpu_gauge = GaugeWidget("CPU 使用率", max_val=100, color=COLORS["blue_main"])
        grid.addWidget(self.cpu_gauge, 0, 0)
        
        self.memory_gauge = GaugeWidget("内存 使用率", max_val=100, color=COLORS["success"])
        grid.addWidget(self.memory_gauge, 0, 1)
        
        self.disk_gauge = GaugeWidget("磁盘 使用率", max_val=100, color=COLORS["warning"])
        grid.addWidget(self.disk_gauge, 0, 2)
        
        # 网络状态
        net_info = QFrame()
        net_layout = QVBoxLayout(net_info)
        self.net_label = QLabel("🌐 网络: 获取中...")
        self.net_label.setFont(QFont(*FONTS["body"]))
        self.net_label.setAlignment(Qt.AlignCenter)
        self.net_label.setStyleSheet(f"color: {COLORS['gray_medium']}; padding: 20px;")
        net_layout.addWidget(self.net_label)
        
        grid.addWidget(net_info, 1, 0, 1, 3)
        
        parent_section.add_layout(grid)
        
    def get_system_info(self):
        """
        获取系统硬件信息
        """
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 尝试获取CPU名称
        try:
            if platform.system() == 'Windows':
                import wmi
                w = wmi.WMI()
                cpu_info = w.Win32_Processor()[0]
                cpu_name = cpu_info.Name.strip()
            else:
                with open('/proc/cpuinfo') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_name = line.split(':')[1].strip()
                            break
        except:
            cpu_name = platform.processor()
            
        if not cpu_name:
            cpu_name = "未知CPU"
            
        def format_bytes(bytes_val):
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_val < 1024:
                    return f"{bytes_val:.1f} {unit}"
                bytes_val /= 1024
            return f"{bytes_val:.1f} PB"
            
        return {
            "cpu_name": cpu_name,
            "cpu_cores": psutil.cpu_count(logical=True),
            "memory_total": format_bytes(mem.total),
            "memory_available": format_bytes(mem.available),
            "disk_total": format_bytes(disk.total),
            "disk_available": format_bytes(disk.free),
            "os_name": platform.system(),
            "os_version": platform.release(),
            "hostname": platform.node()
        }
        
    def get_uptime(self):
        """
        获取系统运行时间
        """
        import datetime
        uptime = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        delta = now - uptime
        
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days}天 {hours}时 {minutes}分"
        
    def on_module_enter(self):
        """
        模块进入时启动监控
        """
        self.start_monitoring()
        
    def on_module_leave(self):
        """
        模块离开时停止监控
        """
        self.stop_monitoring()
        
    def start_monitoring(self):
        """
        启动性能监控
        """
        if self.worker is None:
            self.worker = PerformanceWorker()
            self.worker.data_ready.connect(self.on_data_update)
            self.worker.start()
            
    def stop_monitoring(self):
        """
        停止性能监控
        """
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker = None
            
    def on_data_update(self, data):
        """
        更新性能数据
        """
        self.cpu_gauge.set_value(data["cpu"])
        self.memory_gauge.set_value(data["memory"])
        self.disk_gauge.set_value(data["disk"])
        self.net_label.setText(f"🌐 网络: {data['network']}")
