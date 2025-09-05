"""书签分类管理页面模块"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QScrollArea, QWidget, QDialog, QTextEdit, 
    QFormLayout, QMessageBox, QGridLayout, QSizePolicy, QApplication,
    QComboBox, QColorDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer

from utils.messagebox import NMessageBox
from utils.style import StyleButtonManager
from .base_page import BasePage
from model import BookmarkCategoryManager, BookmarkCategory


class CategoryEditDialog(QDialog):
    """分类编辑对话框"""
    
    def __init__(self, parent=None, category_item: BookmarkCategory = None):
        super().__init__(parent)
        self.category_item = category_item
        self.is_edit_mode = category_item is not None
        
        # 安全地获取颜色
        try:
            self.selected_color = category_item.color if category_item else "#007acc"
        except Exception as e:
            print(f"获取分类颜色时出错: {e}")
            self.selected_color = "#007acc"
        
        # 初始化UI组件引用
        self.color_btn = None
        self.color_label = None
        self.name_edit = None
        self.description_edit = None
        
        self.init_ui()
        
        # 如果是编辑模式，填充现有数据
        if self.is_edit_mode:
            try:
                self.load_data()
            except Exception as e:
                print(f"加载分类数据时出错: {e}")
                import traceback
                traceback.print_exc()
    
    def init_ui(self):
        """初始化对话框UI"""
        self.setWindowTitle("编辑分类" if self.is_edit_mode else "添加分类")
        self.setModal(True)
        self.resize(400, 250)
        
        # 设置对话框特定样式
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
            }
            QFormLayout QLabel {
                color: #333333;
                font-weight: bold;
                margin-bottom: 4px;
            }
            QTextEdit {
                border-radius: 2px;
            }
            QLineEdit{
                border-radius: 2px;
            }
            QPushButton{
                border-radius: 2px;
                border: 1px solid #007acc;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 创建表单
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # 分类名称输入
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入分类名称...")
        form_layout.addRow("名称 *:", self.name_edit)
        
        # 颜色选择
        color_layout = QHBoxLayout()
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(60, 30)
        self.color_btn.clicked.connect(self.choose_color)
        self.update_color_button()
        
        self.color_label = QLabel(self.selected_color)
        self.color_label.setStyleSheet("color: #666666; font-size: 12px;")
        
        color_layout.addWidget(self.color_btn)
        color_layout.addWidget(self.color_label)
        color_layout.addStretch()
        
        form_layout.addRow("颜色:", color_layout)
        
        # 描述输入
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("请输入分类描述...")
        self.description_edit.setMaximumHeight(80)
        form_layout.addRow("描述:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        # 确认按钮
        confirm_btn = QPushButton("确认")
        confirm_btn.clicked.connect(self.accept_data)
        confirm_btn.setObjectName("confirmBtn")
        confirm_btn.setStyleSheet("""
            QPushButton#confirmBtn {
                background-color: #007acc;
                color:white;
            }
            QPushButton#confirmBtn:hover {
                background-color: #005a9e;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)
    
    def update_color_button(self):
        """更新颜色按钮显示"""
        if self.color_btn is not None:
            self.color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.selected_color};
                    border: 2px solid #cccccc;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    border-color: #007acc;
                }}
            """)
        
        if self.color_label is not None:
            self.color_label.setText(self.selected_color)

    def choose_color(self):
        dialog = QColorDialog(QColor(self.selected_color), self)
        dialog.setWindowTitle("选择分类颜色")
        # 修改按钮文字
        for button in dialog.findChildren(QPushButton):
            text = button.text()
            if text == "OK":
                button.setText("确定")
            elif text == "Cancel":
                button.setText("取消")
            elif text == "&Add to Custom Colors":
                button.setText("添加到自定义颜色")
            elif text == "&Pick Screen Color":
                button.setText("选择屏幕颜色")

        # 修改标签文字
        for label in dialog.findChildren(QLabel):
            text=label.text()
            if "&Basic colors" in text:
                label.setText("预设颜色")
            elif "&Custom colors" in text:
                label.setText("我的颜色")

        # 执行并获取结果
        if dialog.exec_():
            color = dialog.selectedColor()
            if color.isValid():
                self.selected_color = color.name()
                self.update_color_button()
    
    def load_data(self):
        """加载现有数据"""
        try:
            if self.category_item:
                if self.name_edit is not None:
                    self.name_edit.setText(getattr(self.category_item, 'name', ''))
                if self.description_edit is not None:
                    self.description_edit.setPlainText(getattr(self.category_item, 'description', ''))
                self.selected_color = getattr(self.category_item, 'color', '#007acc')
                self.update_color_button()
            else:
                print("警告: category_item 为 None")
        except Exception as e:
            print(f"加载分类数据时发生异常: {e}")
            import traceback
            traceback.print_exc()
            # 设置默认值
            if self.name_edit is not None:
                self.name_edit.setText('')
            if self.description_edit is not None:
                self.description_edit.setPlainText('')
            self.selected_color = '#007acc'
            self.update_color_button()
    
    def accept_data(self):
        """确认数据"""
        try:
            name = self.name_edit.text().strip() if self.name_edit else ""
            
            if not name:
                NMessageBox.warning(self, "输入错误", "分类名称不能为空！")
                return
            
            self.accept()
        except Exception as e:
            print(f"确认数据时发生异常: {e}")
            NMessageBox.critical(self, "错误", f"数据验证失败：{str(e)}")
    
    def get_data(self) -> dict:
        """获取输入的数据"""
        try:
            return {
                'name': self.name_edit.text().strip() if self.name_edit else "",
                'description': self.description_edit.toPlainText().strip() if self.description_edit else "",
                'color': self.selected_color
            }
        except Exception as e:
            print(f"获取数据时发生异常: {e}")
            return {
                'name': "",
                'description': "",
                'color': "#007acc"
            }


class BookmarkCategoryManagerPage(BasePage):
    """书签分类管理页面"""

    def __init__(self, encryption_key: str = None):
        super().__init__("书签分类管理")
        self.category_manager = BookmarkCategoryManager()

        # 如果提供了加密密钥，设置加密模式
        if encryption_key:
            self.category_manager.set_encryption_key(encryption_key)

        # 设置QMessageBox的全局样式
        self.setup_messagebox_style()

        # 初始化完成后加载数据
        QTimer.singleShot(0, self.load_categories)
    
    def setup_messagebox_style(self):
        """设置QMessageBox的全局样式"""
        app = QApplication.instance()
        if app:
            # 获取当前应用的样式表
            current_style = app.styleSheet()
            
            # 添加或更新QMessageBox样式
            messagebox_style = """
            /* QMessageBox 全局样式 */
            QMessageBox {
                background-color: #ffffff;
                color: #333333;
                border-radius: 8px;
                font-family: "Microsoft YaHei";
            }
            
            /* QMessageBox 按钮样式 */
            QMessageBox QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
                font-family: "Microsoft YaHei";
            }
            
            QMessageBox QPushButton:hover {
                background-color: #005a9e;
            }
            
            QMessageBox QPushButton:pressed {
                background-color: #004080;
            }
            
            /* QMessageBox 文本样式 */
            QMessageBox QLabel {
                color: #333333;
                font-size: 14px;
                font-family: "Microsoft YaHei";
            }
            
            /* QMessageBox 图标区域 */
            QMessageBox QLabel[objectName="qt_msgbox_label"] {
                color: #333333;
            }
            """
            
            # 合并样式表
            if "QMessageBox" not in current_style:
                app.setStyleSheet(current_style + messagebox_style)
    
    def init_ui(self):
        """初始化分类管理界面"""
        # 清除默认布局
        for i in reversed(range(self.main_layout.count())): 
            self.main_layout.itemAt(i).widget().setParent(None)
        
        # 功能区（上半部分）
        self.create_function_area()
        # 分类展示区（下半部分）
        self.create_category_display_area()
    
    def create_function_area(self):
        """创建功能区"""
        function_frame = QFrame()
        function_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
            }
        """)
        function_frame.setFixedHeight(50)
        layout = QHBoxLayout(function_frame)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # 标题标签
        title_label = QLabel("分类管理")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setStyleSheet("color: #333333;")
        
        # 新增按钮
        add_btn = QPushButton("新增")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e9fff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 2px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1e9fff;
            }
        """)
        add_btn.setFixedHeight(34)
        add_btn.clicked.connect(self.add_category)
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e9fff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 2px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1e9fff;
            }
        """)
        refresh_btn.setFixedHeight(34)
        refresh_btn.clicked.connect(self.load_categories)
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(add_btn)
        layout.addWidget(refresh_btn)
        
        self.main_layout.addWidget(function_frame)
    
    def create_category_display_area(self):
        """创建分类展示区"""
        # 创建显示区域容器
        display_container = QFrame()
        display_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: none;
            }
        """)
        
        container_layout = QVBoxLayout(display_container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        
        # 创建表格
        self.category_table = QTableWidget()
        self.category_table.setColumnCount(4)
        self.category_table.setHorizontalHeaderLabels(["名称", "颜色", "描述", "操作"])
        
        # 设置表格样式
        self.category_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #ffffff;
                gridline-color: #f0f0f0;
                font-family: "Microsoft YaHei";
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #333333;
            }
        """)
        
        # 设置表格属性
        self.category_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.category_table.setAlternatingRowColors(True)
        self.category_table.verticalHeader().setVisible(False)
        
        # 设置行高
        self.category_table.verticalHeader().setDefaultSectionSize(50)
        
        # 设置列宽
        header = self.category_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 名称列
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # 颜色列
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 描述列
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # 操作列
        
        self.category_table.setColumnWidth(1, 100)  # 颜色列宽度
        self.category_table.setColumnWidth(3, 150)  # 操作列宽度
        
        container_layout.addWidget(self.category_table)
        
        self.main_layout.addWidget(display_container)
    
    def load_categories(self):
        """加载所有分类"""
        try:
            self.category_manager.load_data()
            categories = self.category_manager.get_all_categories()
            self.update_category_display(categories)
        except Exception as e:
            if "访问密码错误" in str(e):
                NMessageBox.critical(self, "访问密码错误",
                                     "无法解密分类数据！\n\n可能原因：\n"
                                     "1. 输入的访问密码与之前设置的不一致\n"
                                     "2. 加密文件已损坏\n\n"
                                     "请重新启动程序并输入正确的访问密码。")
                return
            else:
                NMessageBox.critical(self, "加载失败", f"加载分类数据时发生错误：\n{str(e)}")
    
    def update_category_display(self, categories):
        """更新分类显示"""
        self.category_table.setRowCount(len(categories))
        
        for row, category in enumerate(categories):
            # 名称列
            name_item = QTableWidgetItem(category.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # 设置为不可编辑
            self.category_table.setItem(row, 0, name_item)
            
            # 颜色列
            color_widget = QWidget()
            color_layout = QHBoxLayout(color_widget)
            color_layout.setContentsMargins(8, 4, 8, 4)
            
            color_label = QLabel()
            color_label.setFixedSize(20, 20)
            color_label.setStyleSheet(f"""
                background-color: {category.color};
                border: 1px solid #cccccc;
                border-radius: 10px;
            """)
            
            color_text = QLabel(category.color)
            color_text.setStyleSheet("color: #666666; font-size: 11px;")
            
            color_layout.addWidget(color_label)
            color_layout.addWidget(color_text)
            color_layout.addStretch()
            
            self.category_table.setCellWidget(row, 1, color_widget)
            
            # 描述列
            desc_item = QTableWidgetItem(category.description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemIsEditable)
            self.category_table.setItem(row, 2, desc_item)
            
            # 操作列
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)
            action_layout.setSpacing(4)
            
            # 编辑按钮
            edit_btn = QPushButton("编辑")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 2px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            edit_btn.clicked.connect(lambda checked, cat=category: self.edit_category(cat))
            
            # 删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 2px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            delete_btn.clicked.connect(lambda checked, cat=category: self.delete_category(cat))
            
            # 如果是默认分类，禁用删除按钮
            if category.name == "默认分类":
                delete_btn.setEnabled(False)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #cccccc;
                        color: #666666;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 2px;
                        font-size: 11px;
                    }
                """)
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            
            self.category_table.setCellWidget(row, 3, action_widget)
    
    def add_category(self):
        """添加分类"""
        dialog = CategoryEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.category_manager.add_category(
                    name=data['name'],
                    description=data['description'],
                    color=data['color']
                )
                self.load_categories()
                NMessageBox.information(self, "成功", "分类添加成功！")
            except ValueError as e:
                NMessageBox.warning(self, "添加失败", str(e))
            except Exception as e:
                NMessageBox.critical(self, "错误", f"添加分类时发生错误：\n{str(e)}")
    
    def edit_category(self, category: BookmarkCategory):
        """编辑分类"""
        try:
            dialog = CategoryEditDialog(self, category)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                try:
                    # 添加调试信息
                    print(f"正在更新分类: {category.name} -> {data['name']}")
                    result = self.category_manager.update_category(
                        item_id=category.id,
                        name=data['name'],
                        description=data['description'],
                        color=data['color']
                    )
                    if result:
                        self.load_categories()
                        NMessageBox.information(self, "成功", "分类更新成功！")
                    else:
                        NMessageBox.warning(self, "更新失败", "未找到要更新的分类")
                except ValueError as e:
                    NMessageBox.warning(self, "更新失败", str(e))
                except Exception as e:
                    print(f"更新分类时发生异常: {e}")
                    import traceback
                    traceback.print_exc()
                    NMessageBox.critical(self, "错误", f"更新分类时发生错误：\n{str(e)}")
        except Exception as e:
            print(f"编辑分类对话框异常: {e}")
            import traceback
            traceback.print_exc()
            NMessageBox.critical(self, "错误", f"打开编辑对话框时发生错误：\n{str(e)}")
    
    def delete_category(self, category: BookmarkCategory):
        """删除分类"""
        reply = NMessageBox.question(
            self,
            "确认删除",
            f"确定要删除分类 '{category.name}' 吗？\n\n注意：删除分类后，该分类下的书签将被移动到默认分类。\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.category_manager.delete_category(category.id)
                self.load_categories()
                NMessageBox.information(self, "成功", "分类删除成功！")
            except ValueError as e:
                NMessageBox.warning(self, "删除失败", str(e))
            except Exception as e:
                NMessageBox.critical(self, "错误", f"删除分类时发生错误：\n{str(e)}")
