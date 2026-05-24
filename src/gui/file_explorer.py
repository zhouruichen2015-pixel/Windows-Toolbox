# File Explorer Module - 资源管理器模块
# 文件系统浏览和管理，包含文件检索

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter, QLineEdit, QFileDialog, QMessageBox,
    QComboBox, QSpinBox, QMenu, QAction, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QFileInfo
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING

import os
import shutil
import time
from datetime import datetime


class FileSearchWorker(QThread):
    """
    文件搜索线程
    """
    found = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    
    def __init__(self, search_path, keyword, filters=None):
        super().__init__()
        self.search_path = search_path
        self.keyword = keyword.lower()
        self.filters = filters or {}
        self.results = []
        
    def run(self):
        count = 0
        for root, dirs, files in os.walk(self.search_path):
            for name in files + dirs:
                if self.keyword in name.lower():
                    full_path = os.path.join(root, name)
                    if self.pass_filters(full_path):
                        self.found.emit(full_path)
                        self.results.append(full_path)
                count += 1
                if count % 100 == 0:
                    self.progress.emit(len(self.results))
        
        self.finished.emit(self.results)
        
    def pass_filters(self, path):
        """
        应用高级过滤条件
        """
        # 文件类型过滤
        if 'ext' in self.filters and self.filters['ext']:
            ext = os.path.splitext(path)[1].lower()
            if ext not in [e.strip().lower() for e in self.filters['ext'].split(',')]:
                return False
                
        # 文件大小过滤
        if 'max_size' in self.filters and os.path.isfile(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb > self.filters['max_size']:
                return False
                
        return True


class FileExplorerModule(BaseModule):
    """
    资源管理器模块
    """
    module_name = "资源管理器"
    module_icon = "📁"
    
    def __init__(self, parent=None):
        self.current_path = os.path.expanduser("~")
        self.clipboard = None
        self.clipboard_action = None
        self.status_label = None  # 提前初始化，避免初始化顺序问题
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
        
        # 工具栏和搜索栏容器
        toolbar_container = QWidget()
        toolbar_container.setStyleSheet("background-color: #f5f5f5; border-radius: 8px; padding: 10px;")
        toolbar_layout = QVBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # 工具栏
        self.setup_toolbar(toolbar_layout)
        
        # 搜索栏
        self.setup_search_bar(toolbar_layout)
        
        layout.addWidget(toolbar_container)
        
        # 内容区 - 树形目录 + 文件列表
        content_splitter = QSplitter(Qt.Horizontal)
        
        # 左侧目录树
        tree_section = SectionCard("📂 目录树")
        self.setup_tree_view(tree_section)
        content_splitter.addWidget(tree_section)
        
        # 右侧文件列表
        file_section = SectionCard("📄 文件列表")
        self.setup_file_list(file_section)
        content_splitter.addWidget(file_section)
        
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 3)
        
        layout.addWidget(content_splitter)
        
        # 底部状态栏
        self.status_label = QLabel(f"当前路径: {self.current_path}")
        self.status_label.setFont(QFont(*FONTS["body_small"]))
        self.status_label.setStyleSheet(f"color: {COLORS['gray_medium']}; padding: 10px;")
        layout.addWidget(self.status_label)
        
    def setup_toolbar(self, parent_layout):
        """
        配置工具栏
        """
        toolbar_layout = QHBoxLayout()
        
        # 路径操作按钮
        self.back_btn = QPushButton("⬅️ 上一级")
        self.back_btn.clicked.connect(self.go_up)
        toolbar_layout.addWidget(self.back_btn)
        
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.clicked.connect(self.refresh_current)
        toolbar_layout.addWidget(self.refresh_btn)
        
        toolbar_layout.addSpacing(20)
        
        # 文件操作按钮
        self.new_folder_btn = QPushButton("📁 新建文件夹")
        self.new_folder_btn.clicked.connect(self.create_folder)
        toolbar_layout.addWidget(self.new_folder_btn)
        
        self.copy_btn = QPushButton("📋 复制")
        self.copy_btn.clicked.connect(lambda: self.set_clipboard("copy"))
        toolbar_layout.addWidget(self.copy_btn)
        
        self.cut_btn = QPushButton("✂️ 剪切")
        self.cut_btn.clicked.connect(lambda: self.set_clipboard("cut"))
        toolbar_layout.addWidget(self.cut_btn)
        
        self.paste_btn = QPushButton("📌 粘贴")
        self.paste_btn.clicked.connect(self.paste_items)
        self.paste_btn.setEnabled(False)
        toolbar_layout.addWidget(self.paste_btn)
        
        self.delete_btn = QPushButton("🗑️ 删除")
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setProperty("class", "danger")
        toolbar_layout.addWidget(self.delete_btn)
        
        toolbar_layout.addStretch()
        
        # 视图切换
        view_label = QLabel("视图:")
        toolbar_layout.addWidget(view_label)
        
        self.view_combo = QComboBox()
        self.view_combo.addItems(["详细信息", "列表"])
        self.view_combo.currentIndexChanged.connect(self.refresh_current)
        toolbar_layout.addWidget(self.view_combo)
        
        parent_layout.addLayout(toolbar_layout)
        
    def setup_search_bar(self, parent_layout):
        """
        配置搜索栏
        """
        search_layout = QHBoxLayout()
        
        # 搜索输入
        search_label = QLabel("🔍 搜索:")
        search_label.setFont(QFont(*FONTS["body"]))
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入文件名关键词...")
        self.search_input.returnPressed.connect(self.start_search)
        search_layout.addWidget(self.search_input, 1)
        
        # 搜索按钮
        self.search_btn = QPushButton("🔍 开始搜索")
        self.search_btn.clicked.connect(self.start_search)
        search_layout.addWidget(self.search_btn)
        
        search_layout.addSpacing(20)
        
        # 高级过滤选项
        ext_label = QLabel("后缀:")
        search_layout.addWidget(ext_label)
        
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("如: .py,.txt")
        search_layout.addWidget(self.ext_input)
        
        size_label = QLabel("最大MB:")
        search_layout.addWidget(size_label)
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 100000)
        self.size_spin.setValue(1000)
        self.size_spin.setSuffix(" MB")
        search_layout.addWidget(self.size_spin)
        
        parent_layout.addLayout(search_layout)
        
    def setup_tree_view(self, parent_section):
        """
        配置目录树
        """
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_tree_select)
        self.refresh_tree()
        parent_section.add_widget(self.tree)
        
    def setup_file_list(self, parent_section):
        """
        配置文件列表
        """
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(["名称", "大小", "类型", "修改时间", "权限"])
        self.file_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.file_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.file_table.itemDoubleClicked.connect(self.on_file_double_click)
        
        header = self.file_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            
        self.refresh_file_list()
        parent_section.add_widget(self.file_table)
        
    def refresh_tree(self):
        """
        刷新目录树
        """
        self.tree.clear()
        
        # 添加系统根节点
        root_item = QTreeWidgetItem(self.tree, ["此电脑"])
        
        # 添加驱动器
        if os.name == 'nt':
            for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                path = f"{drive}:/"
                if os.path.exists(path):
                    item = QTreeWidgetItem(root_item, [f"{drive}:"])
                    item.setData(0, Qt.UserRole, path)
                    
        # 展开根
        root_item.setExpanded(True)
        
        # 设置当前路径
        self.navigate_to(self.current_path)
        
    def navigate_to(self, path):
        """
        导航到指定路径
        """
        if not os.path.exists(path):
            path = os.path.expanduser("~")

        self.current_path = path
        if self.status_label:
            self.status_label.setText(f"当前路径: {self.current_path}")
        if hasattr(self, 'file_table') and self.file_table is not None:
            self.refresh_file_list()
        
    def refresh_file_list(self):
        """
        刷新文件列表
        """
        if not hasattr(self, 'file_table') or self.file_table is None:
            return

        try:
            items = os.listdir(self.current_path)
        except:
            items = []

        self.file_table.setRowCount(0)
        
        rows = []
        for item_name in items:
            full_path = os.path.join(self.current_path, item_name)
            stat_info = os.stat(full_path)
            
            size = self.format_size(stat_info.st_size)
            mod_time = datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            if os.path.isdir(full_path):
                item_type = "📁 文件夹"
                size = "-"
            else:
                ext = os.path.splitext(item_name)[1].lower()
                if ext in ['.txt', '.md']:
                    item_type = "📄 文档"
                elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    item_type = "🖼️ 图片"
                elif ext in ['.py', '.js', '.html', '.css']:
                    item_type = "💻 代码"
                elif ext in ['.exe', '.msi']:
                    item_type = "⚙️ 程序"
                else:
                    item_type = "📎 文件"
                    
            rows.append({
                "name": item_name,
                "size": size,
                "type": item_type,
                "modified": mod_time,
                "path": full_path
            })
            
        # 先排文件夹，再排文件
        rows.sort(key=lambda x: (x['type'] != "📁 文件夹", x['name'].lower()))
        
        # 添加到表格
        self.file_table.setRowCount(len(rows))
        for i, row_data in enumerate(rows):
            self.file_table.setItem(i, 0, QTableWidgetItem(row_data['name']))
            self.file_table.setItem(i, 1, QTableWidgetItem(row_data['size']))
            self.file_table.setItem(i, 2, QTableWidgetItem(row_data['type']))
            self.file_table.setItem(i, 3, QTableWidgetItem(row_data['modified']))
            self.file_table.setItem(i, 4, QTableWidgetItem("rwx"))
            
    def on_tree_select(self, item):
        """
        目录树选择
        """
        path = item.data(0, Qt.UserRole)
        if path:
            self.navigate_to(path)
            
    def on_file_double_click(self, item):
        """
        文件双击
        """
        row = item.row()
        name = self.file_table.item(row, 0).text()
        full_path = os.path.join(self.current_path, name)
        
        if os.path.isdir(full_path):
            self.navigate_to(full_path)
        else:
            os.startfile(full_path)
            
    def go_up(self):
        """
        上一级
        """
        parent = os.path.dirname(self.current_path)
        if parent != self.current_path and os.path.exists(parent):
            self.navigate_to(parent)
            
    def refresh_current(self):
        """
        刷新当前路径
        """
        self.refresh_file_list()
        
    def create_folder(self):
        """
        新建文件夹
        """
        name, ok = QInputDialog.getText(self, "新建文件夹", "文件夹名称:")
        if ok and name:
            new_path = os.path.join(self.current_path, name)
            try:
                os.makedirs(new_path)
                self.refresh_file_list()
                QMessageBox.information(self, "成功", "文件夹创建成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"创建失败: {str(e)}")
                
    def get_selected_paths(self):
        """
        获取选中文件路径列表
        """
        selected = self.file_table.selectedItems()
        if not selected:
            return []
            
        paths = []
        for row in set(item.row() for item in selected):
            name = self.file_table.item(row, 0).text()
            paths.append(os.path.join(self.current_path, name))
        return paths
        
    def set_clipboard(self, action):
        """
        设置剪贴板
        """
        paths = self.get_selected_paths()
        if not paths:
            QMessageBox.information(self, "提示", "请先选择文件")
            return
            
        self.clipboard = paths
        self.clipboard_action = action
        self.paste_btn.setEnabled(True)
        
        action_text = "复制" if action == "copy" else "剪切"
        QMessageBox.information(self, "提示", f"已{action_text} {len(paths)} 项")
        
    def paste_items(self):
        """
        粘贴项
        """
        if not self.clipboard:
            return
            
        for src in self.clipboard:
            if not os.path.exists(src):
                continue
                
            name = os.path.basename(src)
            dest = os.path.join(self.current_path, name)
            
            # 如果目标已存在，处理冲突
            counter = 1
            while os.path.exists(dest):
                base, ext = os.path.splitext(name)
                dest = os.path.join(self.current_path, f"{base}_{counter}{ext}")
                counter += 1
                
            try:
                if os.path.isdir(src):
                    if self.clipboard_action == "cut":
                        shutil.move(src, dest)
                    else:
                        shutil.copytree(src, dest)
                else:
                    if self.clipboard_action == "cut":
                        shutil.move(src, dest)
                    else:
                        shutil.copy2(src, dest)
                        
            except Exception as e:
                QMessageBox.warning(self, "警告", f"操作失败: {str(e)}")
                
        if self.clipboard_action == "cut":
            self.clipboard = None
            self.clipboard_action = None
            self.paste_btn.setEnabled(False)
            
        self.refresh_file_list()
        
    def delete_selected(self):
        """
        删除选中项
        """
        paths = self.get_selected_paths()
        if not paths:
            QMessageBox.information(self, "提示", "请先选择文件")
            return
            
        confirm = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除 {len(paths)} 项吗？此操作无法恢复！",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return
            
        for path in paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                QMessageBox.warning(self, "警告", f"删除失败: {str(e)}")
                
        self.refresh_file_list()
        
    def start_search(self):
        """
        开始搜索
        """
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.information(self, "提示", "请输入搜索关键词")
            return
            
        # 创建搜索结果临时区域显示
        filters = {
            'ext': self.ext_input.text(),
            'max_size': self.size_spin.value()
        }
        
        # 直接使用搜索对话框或跳转
        search_path = QFileDialog.getExistingDirectory(self, "选择搜索路径", self.current_path)
        if not search_path:
            return
            
        # 显示搜索结果（简单实现 - 跳转）
        self.status_label.setText(f"正在搜索 {keyword}...")
        
        self.search_worker = FileSearchWorker(search_path, keyword, filters)
        self.search_worker.finished.connect(self.on_search_finished)
        self.search_worker.start()
        
    def on_search_finished(self, results):
        """
        搜索完成
        """
        msg = f"找到 {len(results)} 个结果！前10个已显示在文件列表中。"
        
        # 显示前几个结果
        if len(results) > 20:
            results = results[:20]
            
        # 临时在文件列表显示搜索结果
        self.show_search_results(results)
        QMessageBox.information(self, "搜索完成", msg)
        
    def show_search_results(self, results):
        """
        显示搜索结果
        """
        self.file_table.setRowCount(len(results))
        
        for i, path in enumerate(results):
            name = os.path.basename(path)
            size = self.format_size(os.path.getsize(path)) if os.path.isfile(path) else "-"
            mod_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
            
            self.file_table.setItem(i, 0, QTableWidgetItem(name))
            self.file_table.setItem(i, 1, QTableWidgetItem(size))
            self.file_table.setItem(i, 2, QTableWidgetItem("🔍 搜索结果"))
            self.file_table.setItem(i, 3, QTableWidgetItem(mod_time))
            self.file_table.setItem(i, 4, QTableWidgetItem(path))
            
    def format_size(self, bytes_val):
        """
        格式化文件大小
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024
        return f"{bytes_val:.1f} TB"
