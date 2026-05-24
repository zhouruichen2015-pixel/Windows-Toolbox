# Registry Editor Module - 注册表修改器模块
# 注册表查看和编辑

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter, QLineEdit, QMenu, QAction,
    QMessageBox, QInputDialog, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .base_module import BaseModule
from .card_widget import CardWidget, InfoCard, StatCard, SectionCard
from .styles import COLORS, FONTS, SPACING

import os

# 仅在Windows下导入winreg
if os.name == 'nt':
    import winreg
    REGISTRY_AVAILABLE = True
else:
    REGISTRY_AVAILABLE = False


class RegistryEditorModule(BaseModule):
    """
    注册表修改器模块
    """
    module_name = "注册表修改器"
    module_icon = "📝"
    
    def __init__(self, parent=None):
        self.current_hkey = None
        self.current_subkey = None
        self.history = []
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
        
        if not REGISTRY_AVAILABLE:
            info = InfoCard(
                title="⚠️ 不可用",
                subtitle="注册表编辑器仅支持Windows系统",
                icon="❌"
            )
            layout.addWidget(info)
            layout.addStretch()
            return
            
        # 警告提示
        warning = InfoCard(
            title="⚠️  警告",
            subtitle="修改注册表可能导致系统问题，请小心操作",
            icon="📌"
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
        
        # 内容区
        content_splitter = QSplitter(Qt.Horizontal)
        
        # 注册表树
        tree_section = SectionCard("📂 注册表项")
        self.setup_registry_tree(tree_section)
        content_splitter.addWidget(tree_section)
        
        # 键值列表
        value_section = SectionCard("📋 键值列表")
        self.setup_value_table(value_section)
        content_splitter.addWidget(value_section)
        
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 2)
        
        layout.addWidget(content_splitter)
        
    def setup_toolbar(self, parent_layout):
        """
        配置工具栏
        """
        toolbar_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("⬅️ 返回")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        toolbar_layout.addWidget(self.back_btn)
        
        self.new_key_btn = QPushButton("➕ 新建项")
        self.new_key_btn.clicked.connect(self.create_key)
        toolbar_layout.addWidget(self.new_key_btn)
        
        self.new_value_btn = QPushButton("➕ 新建值")
        self.new_value_btn.clicked.connect(self.create_value)
        toolbar_layout.addWidget(self.new_value_btn)
        
        self.edit_btn = QPushButton("✏️ 修改值")
        self.edit_btn.clicked.connect(self.edit_value)
        toolbar_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ 删除")
        self.delete_btn.setProperty("class", "danger")
        self.delete_btn.clicked.connect(self.delete_selected)
        toolbar_layout.addWidget(self.delete_btn)
        
        toolbar_layout.addStretch()
        
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.clicked.connect(self.refresh_current)
        toolbar_layout.addWidget(self.refresh_btn)
        
        parent_layout.addLayout(toolbar_layout)
        
    def setup_search_bar(self, parent_layout):
        """
        配置搜索栏
        """
        search_layout = QHBoxLayout()
        
        search_label = QLabel("🔍 搜索:")
        search_label.setFont(QFont(*FONTS["body"]))
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索注册表项或值名...")
        search_layout.addWidget(self.search_input, 1)
        
        self.search_btn = QPushButton("🔍 搜索")
        self.search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_btn)
        
        parent_layout.addLayout(search_layout)
        
    def setup_registry_tree(self, parent_section):
        """
        配置注册表树形视图
        """
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_tree_select)
        
        # 添加根节点
        root_items = [
            ("HKEY_CLASSES_ROOT", winreg.HKEY_CLASSES_ROOT),
            ("HKEY_CURRENT_USER", winreg.HKEY_CURRENT_USER),
            ("HKEY_LOCAL_MACHINE", winreg.HKEY_LOCAL_MACHINE),
            ("HKEY_USERS", winreg.HKEY_USERS),
            ("HKEY_CURRENT_CONFIG", winreg.HKEY_CURRENT_CONFIG)
        ]
        
        for name, hkey in root_items:
            item = QTreeWidgetItem(self.tree, [name])
            item.setData(0, Qt.UserRole, (hkey, name))
            self.add_dummy_child(item)
            
        parent_section.add_widget(self.tree)
        
    def add_dummy_child(self, item):
        """
        添加虚拟子项以便展开
        """
        QTreeWidgetItem(item, [""])
        
    def on_tree_select(self, item):
        """
        树节点选择
        """
        data = item.data(0, Qt.UserRole)
        if not data:
            return
            
        hkey, path = data
        
        # 展开子项
        self.populate_children(item, hkey, path)
        
        self.current_hkey = hkey
        self.current_subkey = path
        
        # 历史记录
        if path not in [h[1] for h in self.history]:
            self.history.append((hkey, path))
            self.back_btn.setEnabled(len(self.history) > 1)
            
        # 加载键值
        self.load_values(hkey, path)
        
    def populate_children(self, item, hkey, path):
        """
        加载子项
        """
        # 先清空
        while item.childCount() > 0:
            item.removeChild(item.child(0))
            
        try:
            key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, i)
                    child = QTreeWidgetItem(item, [subkey])
                    full_path = path + "\\" + subkey if path else subkey
                    child.setData(0, Qt.UserRole, (hkey, full_path))
                    self.add_dummy_child(child)
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except:
            pass
            
    def setup_value_table(self, parent_section):
        """
        配置键值列表
        """
        self.value_table = QTableWidget()
        self.value_table.setColumnCount(3)
        self.value_table.setHorizontalHeaderLabels(["名称", "类型", "数据"])
        self.value_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.value_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        header = self.value_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        parent_section.add_widget(self.value_table)
        
    def load_values(self, hkey, path):
        """
        加载键值列表
        """
        self.value_table.setRowCount(0)
        
        try:
            key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
            i = 0
            values = []
            while True:
                try:
                    name, value, val_type = winreg.EnumValue(key, i)
                    if not name:
                        name = "(默认)"
                    values.append({
                        "name": name,
                        "type": self.reg_type_to_str(val_type),
                        "data": str(value),
                        "raw_type": val_type,
                        "raw_value": value
                    })
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
            
            # 填充表格
            self.value_table.setRowCount(len(values))
            for row, val in enumerate(values):
                self.value_table.setItem(row, 0, QTableWidgetItem(val["name"]))
                self.value_table.setItem(row, 1, QTableWidgetItem(val["type"]))
                self.value_table.setItem(row, 2, QTableWidgetItem(val["data"]))
                self.value_table.item(row, 0).setData(Qt.UserRole, val)
                
        except Exception as e:
            pass
            
    def reg_type_to_str(self, val_type):
        """
        转换注册表类型为字符串
        """
        types = {
            winreg.REG_SZ: "REG_SZ",
            winreg.REG_EXPAND_SZ: "REG_EXPAND_SZ",
            winreg.REG_BINARY: "REG_BINARY",
            winreg.REG_DWORD: "REG_DWORD",
            winreg.REG_QWORD: "REG_QWORD",
            winreg.REG_MULTI_SZ: "REG_MULTI_SZ"
        }
        return types.get(val_type, str(val_type))
        
    def go_back(self):
        """
        返回上一级
        """
        if len(self.history) > 1:
            self.history.pop()
            last_hkey, last_path = self.history[-1]
            self.current_hkey = last_hkey
            self.current_subkey = last_path
            self.load_values(last_hkey, last_path)
            self.back_btn.setEnabled(len(self.history) > 1)
            
    def refresh_current(self):
        """
        刷新
        """
        if self.current_hkey and self.current_subkey:
            self.load_values(self.current_hkey, self.current_subkey)
            
    def create_key(self):
        """
        新建注册表项
        """
        if not self.current_hkey or not self.current_subkey:
            QMessageBox.information(self, "提示", "请先选择一个父项")
            return
            
        name, ok = QInputDialog.getText(self, "新建项", "项名称:")
        if not (ok and name):
            return
            
        confirm = QMessageBox.question(
            self, "确认", f"确定要在 {self.current_subkey} 下新建项 {name}？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return
            
        try:
            parent_key = winreg.OpenKey(self.current_hkey, self.current_subkey, 0, winreg.KEY_WRITE)
            winreg.CreateKey(parent_key, name)
            winreg.CloseKey(parent_key)
            QMessageBox.information(self, "成功", "项创建成功")
            self.refresh_current()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"创建失败: {str(e)}")
            
    def create_value(self):
        """
        新建值
        """
        if not self.current_hkey or not self.current_subkey:
            QMessageBox.information(self, "提示", "请先选择一个项")
            return
            
        name, ok = QInputDialog.getText(self, "新建值", "值名称:")
        if not (ok and name):
            return
            
        type_combo = QComboBox()
        type_combo.addItems(["REG_SZ (字符串)", "REG_DWORD (32位)", "REG_BINARY"])
        
        data, ok2 = QInputDialog.getText(self, "新建值", "值数据:")
        if ok2:
            self.write_value(name, data, winreg.REG_SZ)
            
    def edit_value(self):
        """
        编辑值
        """
        selected = self.value_table.selectedItems()
        if not selected:
            QMessageBox.information(self, "提示", "请先选择一个值")
            return
            
        row = selected[0].row()
        val_data = self.value_table.item(row, 0).data(Qt.UserRole)
        
        if not val_data:
            return
            
        current_data = val_data["raw_value"]
        
        new_data, ok = QInputDialog.getText(self, "修改值", "值数据:", text=str(current_data))
        
        if ok:
            self.write_value(val_data["name"], new_data, val_data["raw_type"])
            
    def write_value(self, name, value, val_type):
        """
        写入注册表值
        """
        confirm = QMessageBox.question(
            self, "确认", f"确定要修改值 {name} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return
            
        try:
            key = winreg.OpenKey(self.current_hkey, self.current_subkey, 0, winreg.KEY_WRITE)
            if val_type == winreg.REG_DWORD:
                try:
                    value = int(value)
                except:
                    value = 0
            winreg.SetValueEx(key, name, 0, val_type, value)
            winreg.CloseKey(key)
            QMessageBox.information(self, "成功", "值写入成功")
            self.refresh_current()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"写入失败: {str(e)}")
            
    def delete_selected(self):
        """
        删除选中项
        """
        if not self.current_hkey or not self.current_subkey:
            QMessageBox.information(self, "提示", "请先选择")
            return
            
        selected = self.value_table.selectedItems()
        
        if selected:
            row = selected[0].row()
            val_data = self.value_table.item(row, 0).data(Qt.UserRole)
            if val_data:
                confirm = QMessageBox.question(
                    self, "确认", f"确定要删除值 {val_data['name']}？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if confirm == QMessageBox.Yes:
                    try:
                        key = winreg.OpenKey(self.current_hkey, self.current_subkey, 0, winreg.KEY_WRITE)
                        val_name = val_data['name']
                        if val_name == "(默认)":
                            val_name = ""
                        winreg.DeleteValue(key, val_name)
                        winreg.CloseKey(key)
                        QMessageBox.information(self, "成功", "值删除成功")
                        self.refresh_current()
                    except Exception as e:
                        QMessageBox.warning(self, "错误", f"删除失败: {str(e)}")
                        
    def perform_search(self):
        """
        简单搜索
        """
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.information(self, "提示", "请输入搜索关键词")
            return
            
        QMessageBox.information(self, "搜索", 
                            "搜索功能已禁用（搜索整个注册表会很慢）。请使用目录树导航。")
