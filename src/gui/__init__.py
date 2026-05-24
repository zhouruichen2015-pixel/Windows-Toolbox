#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MHY 工具箱 - GUI 模块
该模块包含程序的图形用户界面相关代码
"""

from .main_window import ZRCMainWindow
from .styles import get_stylesheet, get_sidebar_stylesheet, apply_styles
from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard

# 功能模块
try:
    from .tool_launcher import ToolLauncherModule
except:
    pass

try:
    from .system_monitor import SystemMonitorModule
except:
    pass

try:
    from .task_manager import TaskManagerModule
except:
    pass

try:
    from .file_explorer import FileExplorerModule
except:
    pass

try:
    from .registry_editor import RegistryEditorModule
except:
    pass

try:
    from .file_shredder import FileShredderModule
except:
    pass

try:
    from .virus_scanner import VirusScannerModule
except:
    pass

try:
    from .iso_writer import IsoWriterModule
except:
    pass


__all__ = [
    'ZRCMainWindow',
    'BaseModule',
    'CardWidget',
    'InfoCard',
    'StatCard',
    'SectionCard',
    'get_stylesheet',
    'get_sidebar_stylesheet',
    'apply_styles'
]
