# System Info Module - 系统信息模块
# 显示真实的系统硬件和软件信息

import platform
import psutil
import os
import socket
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .styles import COLORS, FONTS, SPACING
from .card_widget import StatCard, InfoCard, SectionCard


class SystemInfoModule(BaseModule):
    """系统信息模块 - 显示真实的系统硬件和软件信息"""
    
    module_name = "系统信息"
    module_icon = "💻"
    
    def setup_ui(self):
        """设置模块UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(SPACING["card"], SPACING["card"], SPACING["card"], SPACING["card"])
        main_layout.setSpacing(SPACING["card"])
        
        title = QLabel(f"{self.module_icon} {self.module_name}")
        title.setFont(QFont(*FONTS["title_large"]))
        title.setStyleSheet(f"color: {COLORS['blue_dark']};")
        main_layout.addWidget(title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        main_layout.addWidget(scroll_area)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(SPACING["card"])
        scroll_area.setWidget(scroll_content)
        
        self.create_summary_section(scroll_layout)
        self.create_cpu_section(scroll_layout)
        self.create_memory_section(scroll_layout)
        self.create_disk_section(scroll_layout)
        self.create_system_section(scroll_layout)
        self.create_network_section(scroll_layout)
    
    def create_summary_section(self, parent_layout):
        """创建系统概览区域"""
        section = SectionCard("系统概览")
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        cpu_usage = psutil.cpu_percent()
        cpu_card = StatCard(
            title="CPU使用率",
            value=str(cpu_usage),
            unit="%",
            icon="⚙️",
            color=COLORS["blue_main"]
        )
        grid_layout.addWidget(cpu_card, 0, 0)
        
        mem = psutil.virtual_memory()
        mem_usage = mem.percent
        mem_card = StatCard(
            title="内存使用率",
            value=str(mem_usage),
            unit="%",
            icon="🧠",
            color=COLORS["success"]
        )
        grid_layout.addWidget(mem_card, 0, 1)
        
        try:
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
        except:
            disk_usage = 0
        disk_card = StatCard(
            title="磁盘使用率",
            value=str(disk_usage),
            unit="%",
            icon="💿",
            color=COLORS["warning"]
        )
        grid_layout.addWidget(disk_card, 1, 0)
        
        process_count = len(psutil.pids())
        process_card = StatCard(
            title="运行进程数",
            value=str(process_count),
            unit="个",
            icon="📊",
            color=COLORS["blue_dark"]
        )
        grid_layout.addWidget(process_card, 1, 1)
        
        section.add_layout(grid_layout)
        parent_layout.addWidget(section)
    
    def create_cpu_section(self, parent_layout):
        """创建CPU信息区域"""
        section = SectionCard("处理器信息")
        
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)
        
        cpu_info = self.get_cpu_info()
        
        layout.addWidget(QLabel("<b>处理器型号：</b>"), 0, 0)
        cpu_label = QLabel(cpu_info["name"])
        cpu_label.setFont(QFont(*FONTS["body"]))
        layout.addWidget(cpu_label, 0, 1)
        
        layout.addWidget(QLabel("<b>物理核心：</b>"), 1, 0)
        layout.addWidget(QLabel(f"{cpu_info['cores']} 核"), 1, 1)
        
        layout.addWidget(QLabel("<b>逻辑线程：</b>"), 2, 0)
        layout.addWidget(QLabel(f"{cpu_info['threads']} 线程"), 2, 1)
        
        layout.addWidget(QLabel("<b>CPU架构：</b>"), 3, 0)
        layout.addWidget(QLabel(cpu_info["arch"]), 3, 1)
        
        layout.addWidget(QLabel("<b>运行频率：</b>"), 4, 0)
        layout.addWidget(QLabel(cpu_info["freq"]), 4, 1)
        
        section.add_layout(layout)
        parent_layout.addWidget(section)
    
    def create_memory_section(self, parent_layout):
        """创建内存信息区域"""
        section = SectionCard("内存信息")
        
        mem_info = self.get_memory_info()
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)
        
        layout.addWidget(QLabel("<b>总内存：</b>"), 0, 0)
        layout.addWidget(QLabel(mem_info["total"]), 0, 1)
        
        layout.addWidget(QLabel("<b>已使用：</b>"), 1, 0)
        layout.addWidget(QLabel(f"{mem_info['used']} ({mem_info['percent']})"), 1, 1)
        
        layout.addWidget(QLabel("<b>可用内存：</b>"), 2, 0)
        layout.addWidget(QLabel(mem_info["available"]), 2, 1)
        
        layout.addWidget(QLabel("<b>空闲内存：</b>"), 3, 0)
        layout.addWidget(QLabel(mem_info["free"]), 3, 1)
        
        section.add_layout(layout)
        parent_layout.addWidget(section)
    
    def create_disk_section(self, parent_layout):
        """创建磁盘信息区域"""
        section = SectionCard("磁盘信息")
        
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)
        
        disks = self.get_disk_info()
        row = 0
        for disk in disks:
            layout.addWidget(QLabel(f"<b>{disk['name']}：</b>"), row, 0)
            layout.addWidget(QLabel(f"{disk['total']}"), row, 1)
            row += 1
            
            layout.addWidget(QLabel("  已使用："), row, 0)
            layout.addWidget(QLabel(f"{disk['used']} ({disk['percent']})"), row, 1)
            row += 1
            
            layout.addWidget(QLabel("  可用空间："), row, 0)
            layout.addWidget(QLabel(disk['free']), row, 1)
            row += 1
        
        section.add_layout(layout)
        parent_layout.addWidget(section)
    
    def create_system_section(self, parent_layout):
        """创建操作系统信息区域"""
        section = SectionCard("系统信息")
        
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)
        
        os_info = self.get_os_info()
        
        layout.addWidget(QLabel("<b>操作系统：</b>"), 0, 0)
        layout.addWidget(QLabel(os_info["name"]), 0, 1)
        
        layout.addWidget(QLabel("<b>系统版本：</b>"), 1, 0)
        layout.addWidget(QLabel(os_info["version"]), 1, 1)
        
        layout.addWidget(QLabel("<b>系统位数：</b>"), 2, 0)
        layout.addWidget(QLabel(os_info["arch"]), 2, 1)
        
        layout.addWidget(QLabel("<b>计算机名：</b>"), 3, 0)
        layout.addWidget(QLabel(os_info["hostname"]), 3, 1)
        
        layout.addWidget(QLabel("<b>IP地址：</b>"), 4, 0)
        layout.addWidget(QLabel(os_info["ip"]), 4, 1)
        
        layout.addWidget(QLabel("<b>启动时间：</b>"), 5, 0)
        layout.addWidget(QLabel(os_info["boot_time"]), 5, 1)
        
        layout.addWidget(QLabel("<b>Python版本：</b>"), 6, 0)
        layout.addWidget(QLabel(platform.python_version()), 6, 1)
        
        section.add_layout(layout)
        parent_layout.addWidget(section)
    
    def create_network_section(self, parent_layout):
        """创建网络信息区域"""
        section = SectionCard("网络信息")
        
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 5, 10, 5)
        
        net_info = self.get_network_info()
        row = 0
        for name, ip in net_info.items():
            layout.addWidget(QLabel(f"<b>{name}：</b>"), row, 0)
            layout.addWidget(QLabel(ip), row, 1)
            row += 1
        
        section.add_layout(layout)
        parent_layout.addWidget(section)
    
    def get_os_info(self):
        """获取操作系统信息（真实数据）"""
        info = {}
        info["name"] = platform.system()
        
        try:
            if platform.system() == "Windows":
                info["version"] = platform.win32_ver()[0] + " Build " + platform.win32_ver()[1]
            else:
                info["version"] = platform.version()
        except:
            info["version"] = "未知"
        
        info["arch"] = "64位" if platform.architecture()[0] == "64bit" else "32位"
        info["hostname"] = socket.gethostname()
        info["ip"] = self.get_ip_address()
        info["boot_time"] = self.get_boot_time()
        
        return info
    
    def get_cpu_info(self):
        """获取CPU信息（真实数据）"""
        info = {}
        
        try:
            if platform.system() == "Windows":
                # 方法1: 通过注册表获取CPU信息
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                    info["name"] = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
                    
                    try:
                        freq_mhz = winreg.QueryValueEx(key, "~MHz")[0]
                        info["freq"] = f"{freq_mhz} MHz"
                    except:
                        # 尝试通过wmic获取频率
                        try:
                            result = subprocess.check_output(
                                ["wmic", "cpu", "get", "CurrentClockSpeed"],
                                encoding="utf-8",
                                errors="ignore"
                            )
                            lines = result.strip().split("\n")
                            if len(lines) > 1:
                                freq = lines[1].strip()
                                if freq:
                                    info["freq"] = f"{freq} MHz"
                        except:
                            info["freq"] = "未知"
                    
                    winreg.CloseKey(key)
                except:
                    # 方法2: 直接通过wmic获取
                    try:
                        result = subprocess.check_output(
                            ["wmic", "cpu", "get", "Name"],
                            encoding="utf-8",
                            errors="ignore"
                        )
                        lines = result.strip().split("\n")
                        if len(lines) > 1:
                            info["name"] = lines[1].strip()
                        else:
                            info["name"] = platform.processor() or "未知"
                    except:
                        info["name"] = platform.processor() or "未知"
                
                # 获取核心数和线程数
                try:
                    result = subprocess.check_output(
                        ["wmic", "cpu", "get", "NumberOfCores,NumberOfLogicalProcessors"],
                        encoding="utf-8",
                        errors="ignore"
                    )
                    lines = result.strip().split("\n")
                    if len(lines) > 1:
                        parts = [p.strip() for p in lines[1].split("  ") if p.strip()]
                        if len(parts) >= 2:
                            info["cores"] = int(parts[0])
                            info["threads"] = int(parts[1])
                        else:
                            info["cores"] = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1
                            info["threads"] = psutil.cpu_count() or info["cores"] * 2
                    else:
                        info["cores"] = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1
                        info["threads"] = psutil.cpu_count() or info["cores"] * 2
                except:
                    info["cores"] = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1
                    info["threads"] = psutil.cpu_count() or info["cores"] * 2
                
                info["arch"] = platform.machine()
            else:
                info["name"] = platform.processor() or "未知"
                info["cores"] = os.cpu_count() or 1
                info["threads"] = info["cores"] * 2
                info["freq"] = "未知"
                info["arch"] = platform.machine()
        except Exception as e:
            info["name"] = platform.processor() or "未知"
            info["cores"] = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1
            info["threads"] = psutil.cpu_count() or info["cores"] * 2
            info["freq"] = "未知"
            info["arch"] = platform.machine()
        
        # 确保我们有合理的默认值
        if "name" not in info or info["name"] == "":
            info["name"] = platform.processor() or "未知"
        if "cores" not in info:
            info["cores"] = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1
        if "threads" not in info:
            info["threads"] = psutil.cpu_count() or info["cores"] * 2
        if "freq" not in info:
            info["freq"] = "未知"
        if "arch" not in info:
            info["arch"] = platform.machine()
        
        return info
    
    def get_memory_info(self):
        """获取内存信息（真实数据）"""
        info = {}
        
        try:
            mem = psutil.virtual_memory()
            info["total"] = self.format_bytes(mem.total)
            info["used"] = self.format_bytes(mem.used)
            info["available"] = self.format_bytes(mem.available)
            info["free"] = self.format_bytes(mem.free)
            info["percent"] = f"{mem.percent}%"
        except Exception as e:
            info["total"] = "未知"
            info["used"] = "未知"
            info["available"] = "未知"
            info["free"] = "未知"
            info["percent"] = "未知"
        
        return info
    
    def get_disk_info(self):
        """获取磁盘信息（真实数据）"""
        disks = []
        
        try:
            for part in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    disks.append({
                        "name": part.device,
                        "total": self.format_bytes(usage.total),
                        "used": self.format_bytes(usage.used),
                        "free": self.format_bytes(usage.free),
                        "percent": f"{usage.percent}%"
                    })
                except:
                    continue
            
            if not disks:
                disks.append({"name": "磁盘", "total": "未知", "used": "未知", "free": "未知", "percent": "未知"})
        except:
            disks.append({"name": "磁盘", "total": "未知", "used": "未知", "free": "未知", "percent": "未知"})
        
        return disks
    
    def get_network_info(self):
        """获取网络信息（真实数据）"""
        info = {}
        
        try:
            info["主机名"] = socket.gethostname()
            
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == 2:  # AF_INET
                        info[f"{interface} (IPv4)"] = addr.address
                    elif addr.family == 10:  # AF_INET6
                        ip = addr.address[:30] + "..." if len(addr.address) > 30 else addr.address
                        info[f"{interface} (IPv6)"] = ip
            
            if not info:
                info["主机名"] = socket.gethostname()
                info["IP地址"] = self.get_ip_address()
        except:
            info["主机名"] = socket.gethostname()
            info["IP地址"] = self.get_ip_address()
        
        return info
    
    def get_ip_address(self):
        """获取IP地址（真实数据）"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "未知"
    
    def get_boot_time(self):
        """获取系统启动时间（真实数据）"""
        try:
            boot_time = psutil.boot_time()
            return datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "未知"
    
    def format_bytes(self, bytes_value):
        """格式化字节数"""
        if bytes_value < 1024:
            return f"{bytes_value} B"
        elif bytes_value < 1024 * 1024:
            return f"{bytes_value / 1024:.2f} KB"
        elif bytes_value < 1024 * 1024 * 1024:
            return f"{bytes_value / (1024 * 1024):.2f} MB"
        else:
            return f"{bytes_value / (1024 * 1024 * 1024):.2f} GB"