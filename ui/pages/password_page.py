"""密码管理页面模块"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QScrollArea, QWidget, QDialog, QTextEdit, 
    QFormLayout, QMessageBox, QGridLayout, QLayout, QSizePolicy, QApplication,
    QComboBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QRect, QSize

from utils.messagebox import NMessageBox
from .base_page import BasePage
from model import PasswordManager, PasswordItem




class FlowLayout(QLayout):
    """流式布局类 - 实现卡片自动换行的flex布局效果"""
    
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        else:
            self.setContentsMargins(0, 0, 0, 0)
            
        self.setSpacing(spacing)
        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if index >= 0 and index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
            
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing() if self.spacing() >= 0 else 10

        for item in self._item_list:
            item_size = item.sizeHint()
            next_x = x + item_size.width() + spacing
            
            # 如果当前行放不下这个item，换行
            if next_x - spacing > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + spacing
                next_x = x + item_size.width() + spacing
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(x, y, item_size.width(), item_size.height()))

            x = next_x
            line_height = max(line_height, item_size.height())

        return y + line_height - rect.y()


class PasswordEditDialog(QDialog):
    """密码编辑对话框"""
    
    def __init__(self, parent=None, password_item: PasswordItem = None):
        super().__init__(parent)
        self.password_item = password_item
        self.is_edit_mode = password_item is not None
        
        try:
            self.init_ui()
            
            # 如果是编辑模式，填充现有数据
            if self.is_edit_mode:
                self.load_data()
        except Exception as e:
            print(f"初始化密码编辑对话框时发生异常: {e}")
            import traceback
            traceback.print_exc()
    
    def init_ui(self):
        """初始化对话框UI"""
        self.setWindowTitle("编辑密码" if self.is_edit_mode else "添加密码")
        self.setModal(True)
        self.resize(400, 300)
        
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
        layout.setContentsMargins(20, 20, 20, 20)  # 设置内边距
        layout.setSpacing(16)  # 设置元素间距
        
        # 创建表单
        form_layout = QFormLayout()
        form_layout.setSpacing(12)  # 表单元素间距
        
        # 标题输入
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("请输入标题...")
        form_layout.addRow("标题 *:", self.title_edit)
        
        # 来源输入
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText("请输入来源（如：微信、QQ、网站等）...")
        form_layout.addRow("来源 *:", self.source_edit)
        
        # 账号输入
        self.account_edit = QLineEdit()
        self.account_edit.setPlaceholderText("请输入账号...")
        form_layout.addRow("账号 *:", self.account_edit)
        
        # 密码输入
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码...")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("密码 *:", self.password_edit)
        
        # 描述输入
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("请输入描述...")
        self.description_edit.setMaximumHeight(80)
        form_layout.addRow("描述:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)  # 设置按钮间距
        
        # 显示/隐藏密码按钮
        self.toggle_password_btn = QPushButton("显示")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        self.toggle_password_btn.setObjectName("toggleBtn")
        self.toggle_password_btn.setStyleSheet("""
            QPushButton#toggleBtn {
                background-color: #1e9fff;
                border:none;
                color:white;
            }
            QPushButton#toggleBtn:hover {
                background-color: #007acc;
            }
        """)
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        # 确认按钮
        confirm_btn = QPushButton("确认")
        confirm_btn.clicked.connect(self.accept_data)
        confirm_btn.setObjectName("confirmBtn")  # 设置对象名用于特定样式
        confirm_btn.setStyleSheet("""
            QPushButton#confirmBtn {
                background-color: #1e9fff;
                border:none;
                color:white;
            }
            QPushButton#confirmBtn:hover {
                background-color: #007acc;
            }
        """)
        
        button_layout.addWidget(self.toggle_password_btn)
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        layout.addLayout(button_layout)
    
    def toggle_password_visibility(self):
        """切换密码显示/隐藏"""
        if self.password_edit.echoMode() == QLineEdit.Password:
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("隐藏")
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("显示")
    
    def load_data(self):
        """加载现有数据"""
        try:
            self.title_edit.setText(self.password_item.title)
            self.source_edit.setText(getattr(self.password_item, 'source', ''))  # 兼容旧数据
            self.account_edit.setText(self.password_item.account)
            self.password_edit.setText(self.password_item.password)
            self.description_edit.setPlainText(self.password_item.description)
        except Exception as e:
            print(f"加载密码数据时发生异常: {e}")
            import traceback
            traceback.print_exc()
    
    def accept_data(self):
        """确认数据"""
        title = self.title_edit.text().strip()
        account = self.account_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not title or not account or not password:
            NMessageBox.warning(self, "输入错误", "标题、账号和密码不能为空！")
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """获取输入的数据"""
        return {
            'title': self.title_edit.text().strip(),
            'source': self.source_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'account': self.account_edit.text().strip(),
            'password': self.password_edit.text().strip()
        }


class PasswordCard(QFrame):
    """密码卡片组件"""
    
    def __init__(self, password_item: PasswordItem, parent=None):
        super().__init__(parent)
        self.password_item = password_item
        self.parent_page = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化卡片UI"""
        self.setStyleSheet("""
            QFrame {
                border-radius: 2px;
                border: 1px solid #e4e7ed;
            }
            QFrame:hover {
                border-color: #1e9fff;
            }
        """)
        # 设置固定宽度和高度
        self.setFixedSize(300, 180)  # 增加高度以容纳更多描述文本
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(4)  # 设置组件间的默认间距
        
        # 标题标签 - 独占一行，确保完全显示
        title_label = QLabel(self.password_item.title)
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setStyleSheet("color: black; border:none;")
        title_label.setMaximumHeight(26)  # 设置最小高度
        layout.addWidget(title_label)  # 添加标题标签

        # 来源地址信息行
        url_layout = QHBoxLayout()
        url_layout.setSpacing(4)
        url_layout.setContentsMargins(0, 4, 0, 4)
        url_label = QLabel("地址:")
        url_label.setFont(QFont("Microsoft YaHei", 10))
        url_label.setStyleSheet("color: #666666; border:none;")
        url_label.setFixedWidth(35)
        url_value = QLabel(getattr(self.password_item, 'source', ''))
        url_value.setFont(QFont("Microsoft YaHei", 10))
        url_value.setStyleSheet("color: #28a745; border:none; font-weight: bold;")
        url_layout.addWidget(url_label)
        url_layout.addWidget(url_value, 1)
        layout.addLayout(url_layout)


        # 描述
        description_layout = QHBoxLayout()
        description_layout.setSpacing(4)
        description_layout.setContentsMargins(0, 4, 0, 4)

        description_label = QLabel("描述:")
        description_label.setFont(QFont("Microsoft YaHei", 10))
        description_label.setStyleSheet("color: #666666; border:none;")
        description_label.setFixedWidth(35)
        description_label.setAlignment(Qt.AlignTop)  # 顶部对齐

        description_value = QLabel(getattr(self.password_item, 'description', '无描述'))
        description_value.setFont(QFont("Microsoft YaHei", 9))
        description_value.setStyleSheet("color: #999999; border:none;")
        description_value.setWordWrap(True)
        description_value.setAlignment(Qt.AlignTop)
        description_value.setMinimumHeight(34)
        description_value.setMaximumHeight(34)

        description_layout.addWidget(description_label)
        description_layout.addWidget(description_value, 1)
        layout.addLayout(description_layout)
        # 添加弹性空间
        layout.addStretch()
        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(0, 8, 0, 0)

        # 复制按钮
        copy_btn = QPushButton("复制")
        copy_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #1e9fff;
                            color: white;
                            border: none;
                            padding: 8px 12px;
                            border-radius: 2px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #005a9e;
                        }
                 """)
        copy_btn.clicked.connect(self.copy_password)

        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                        border: none;
                        padding: 8px 12px;
                        border-radius: 2px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
        edit_btn.clicked.connect(self.edit_password)

        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #dc3545;
                        color: white;
                        border: none;
                        padding: 8px 12px;
                        border-radius: 2px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c82333;
                    }
                """)
        delete_btn.clicked.connect(self.delete_password)
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        layout.addLayout(button_layout)

    """复制密码到剪贴板"""
    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_item.password)
        # 显示复制成功提示
        if self.parent_page:
            msg = QMessageBox(self.parent_page)
            msg.setWindowTitle("复制成功")
            msg.setText(f"{self.password_item.title}  的密码已复制到剪贴板")
            # 设置提示框样式
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #ffffff;
                }
                QMessageBox QPushButton {
                    background-color: #1e9fff;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 2px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #1e9fff;
                }
            """)
            # 显示提示并自动关闭
            QTimer.singleShot(2000, msg.close)  # 1.5秒后自动关闭
            msg.exec_()
    
    def edit_password(self):
        """编辑密码"""
        if self.parent_page:
            self.parent_page.edit_password(self.password_item)
    
    def delete_password(self):
        """删除密码"""
        if self.parent_page:
            self.parent_page.delete_password(self.password_item)


class PasswordManagerPage(BasePage):
    """密码管理页面"""

    def __init__(self, encryption_key: str = None):
        super().__init__("密码管理")
        self.password_manager = PasswordManager()
        self.current_passwords = []
        self.current_source = "全部"  # 当前选择的来源筛选

        # 如果提供了加密密钥，设置加密模式
        if encryption_key:
            self.password_manager.set_encryption_key(encryption_key)

        # 设置QMessageBox的全局样式
        self.setup_messagebox_style()

        # 初始化完成后加载数据
        QTimer.singleShot(0, self.load_data)
    
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
                font-size: 12px;
            }
            """
            
            # 合并样式表
            if "QMessageBox" not in current_style:
                app.setStyleSheet(current_style + messagebox_style)
    
    def init_ui(self):
        """初始化密码管理界面"""
        # 清除默认布局
        for i in reversed(range(self.main_layout.count())): 
            self.main_layout.itemAt(i).widget().setParent(None)
        # 功能区（上半部分）
        self.create_function_area()
        # 密码展示区（下半部分）
        self.create_password_display_area()
    
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
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setPlaceholderText("搜索密码（标题、来源、账号、描述）...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 2px;
                font-size: 14px;
                height: 24px;
                background-color: #ffffff;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #007acc;
                outline: none;
            }
        """)
        # 设置搜索框的固定高度
        self.search_edit.setFixedHeight(34)
        self.search_edit.textChanged.connect(self.search_passwords)
        
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
        add_btn.setFixedHeight(34)  # 与搜索框保持一致的高度
        add_btn.clicked.connect(self.add_password)
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
        refresh_btn.setFixedHeight(34)  # 与搜索框保持一致的高度
        refresh_btn.clicked.connect(self.load_data)
        
        layout.addWidget(self.search_edit)
        layout.addWidget(add_btn)
        layout.addWidget(refresh_btn)
        
        self.main_layout.addWidget(function_frame)
    
    def create_password_display_area(self):
        """创建密码展示区"""
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
        
        # 搜索状态标签
        self.search_status_label = QLabel("")
        self.search_status_label.setFont(QFont("Microsoft YaHei", 10))
        self.search_status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                padding: 4px 0px;
                border: none;
            }
        """)
        self.search_status_label.hide()  # 默认隐藏
        container_layout.addWidget(self.search_status_label)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f5f7fa;
                width: 10px;
                border-radius: 5px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c4cc;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #909399;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # 内容widget
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        # 使用流式布局实现flex效果
        self.content_layout = FlowLayout(self.content_widget, margin=4, spacing=12)

        # 创建一个包装器来容纳FlowLayout和提示标签
        self.content_wrapper = QWidget()
        wrapper_layout = QVBoxLayout(self.content_wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addWidget(self.content_widget)
        wrapper_layout.addStretch()
        
        scroll_area.setWidget(self.content_wrapper)
        container_layout.addWidget(scroll_area)
        
        self.main_layout.addWidget(display_container)
        
        # 空状态提示
        self.empty_label = QLabel("暂无密码记录\n点击上方添加密码按钮开始添加", self.content_widget)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setFixedSize(400, 150)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #999999;
                font-size: 16px;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 12px;
                border: none;
            }
        """)
        self.empty_label.hide()
        
        # 搜索无结果提示
        self.no_results_label = QLabel("未找到匹配的密码记录\n请尝试其他关键词", self.content_widget)
        self.no_results_label.setAlignment(Qt.AlignCenter)
        self.no_results_label.setFixedSize(350, 120)
        self.no_results_label.setStyleSheet("""
            QLabel {
                color: #999999;
                font-size: 14px;
                padding: 20px;
                background-color: #fff3cd;
                border-radius: 8px;
                border: none;
            }
        """)
        self.no_results_label.hide()
    
    def load_passwords(self):
        """加载所有密码"""
        try:
            self.password_manager.load_data()
            self.current_passwords = self.password_manager.get_all_passwords()
            self.update_password_display()
        except Exception as e:
            if "访问密码错误" in str(e):
                # 显示密码错误提示，但不清空现有数据
                NMessageBox.critical(self, "访问密码错误",
                                         "无法解密密码数据！\n\n可能原因：\n"
                                         "1. 输入的访问密码与之前设置的不一致\n"
                                         "2. 加密文件已损坏\n\n"
                                         "请重新启动程序并输入正确的访问密码。")
                # 不更新显示，保持当前状态
                return
            else:
                # 其他错误，显示通用错误信息
                NMessageBox.critical(self, "加载失败", f"加载密码数据时发生错误：\n{str(e)}")
                self.current_passwords = []
                self.update_password_display()
    
    def load_data(self):
        """加载所有数据"""
        try:
            # 加载密码数据
            self.password_manager.load_data()
            self.filter_passwords()
        except Exception as e:
            if "访问密码错误" in str(e):
                # 显示密码错误提示，但不清空现有数据
                NMessageBox.critical(self, "访问密码错误",
                                     "无法解密密码数据！\n\n可能原因：\n"
                                     "1. 输入的访问密码与之前设置的不一致\n"
                                     "2. 加密文件已损坏\n\n"
                                     "请重新启动程序并输入正确的访问密码。")
                # 不更新显示，保持当前状态
                return
            else:
                # 其他错误，显示通用错误信息
                NMessageBox.critical(self, "加载失败", f"加载密码数据时发生错误：\n{str(e)}")
                self.current_passwords = []
                self.update_password_display()
    

    def filter_passwords(self):
        """筛选密码（结合来源和搜索）"""
        all_passwords = self.password_manager.get_all_passwords()
        
        # 先按来源筛选
        if self.current_source == "全部":
            filtered_passwords = all_passwords
        else:
            filtered_passwords = [p for p in all_passwords if p.source == self.current_source]
        
        # 再按搜索关键词筛选
        search_query = self.search_edit.text().strip()
        if search_query:
            search_query = search_query.lower()
            self.current_passwords = []
            for item in filtered_passwords:
                if (search_query in item.title.lower() or 
                    search_query in item.source.lower() or
                    search_query in item.account.lower() or
                    search_query in item.description.lower()):
                    self.current_passwords.append(item)
        else:
            self.current_passwords = filtered_passwords
        
        self.update_password_display()
    
    def update_password_display(self):
        """更新密码显示"""
        # 清除FlowLayout中的所有项目
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        # 获取搜索关键词
        search_query = self.search_edit.text().strip()
        total_passwords = len(self.password_manager.get_all_passwords())
        
        # 更新搜索状态
        if search_query:
            # 显示搜索状态
            self.search_status_label.show()
            if self.current_passwords:
                self.search_status_label.setText(f"搜索 \"{search_query}\" 找到 {len(self.current_passwords)} 条记录")
                self.search_status_label.setStyleSheet("""
                    QLabel {
                        color: #28a745;
                        padding: 8px 0px;
                        border: none;
                        font-weight: bold;
                    }
                """)
            else:
                self.search_status_label.setText(f"搜索 \"{search_query}\" 未找到匹配记录")
                self.search_status_label.setStyleSheet("""
                    QLabel {
                        color: #dc3545;
                        padding: 8px 0px;
                        border: none;
                        font-weight: bold;
                    }
                """)
        else:
            # 隐藏搜索状态
            self.search_status_label.hide()
        
        # 显示内容
        if not self.current_passwords:
            # 隐藏另一个提示标签
            self.empty_label.hide()
            self.no_results_label.hide()
            
            # 显示对应的提示标签
            if search_query:
                self.no_results_label.show()
                self.no_results_label.move(25, 25)
            elif total_passwords == 0:
                self.empty_label.show()
                self.empty_label.move(25, 25)
        else:
            # 隐藏提示标签
            self.empty_label.hide()
            self.no_results_label.hide()
            
            # 显示密码卡片（流式布局会自动换行）
            for i, password_item in enumerate(self.current_passwords):
                card = PasswordCard(password_item, self)
                card.setProperty("cardIndex", i)
                self.content_layout.addWidget(card)
        
        # 更新布局
        self.content_widget.update()
    
    def search_passwords(self):
        """搜索密码"""
        self.filter_passwords()
    
    def add_password(self):
        """添加密码"""
        dialog = PasswordEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.password_manager.add_password(
                title=data['title'],
                source=data['source'],
                description=data['description'],
                account=data['account'],
                password=data['password']
            )
            self.load_data()
            NMessageBox.information(self, "成功", "密码添加成功！")
    
    def edit_password(self, password_item: PasswordItem):
        """编辑密码"""
        try:
            dialog = PasswordEditDialog(self, password_item)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                print(f"准备更新密码: {data['title']}")
                
                success = self.password_manager.update_password(
                    item_id=password_item.id,
                    title=data['title'],
                    source=data['source'],
                    description=data['description'],
                    account=data['account'],
                    password=data['password']
                )
                
                if success:
                    print("密码更新成功，重新加载数据...")
                    self.load_data()
                    NMessageBox.information(self, "成功", "密码更新成功！")
                else:
                    print("密码更新失败")
                    NMessageBox.warning(self, "错误", "密码更新失败！")
        except Exception as e:
            print(f"编辑密码时发生异常: {e}")
            import traceback
            traceback.print_exc()
            NMessageBox.critical(self, "错误", f"编辑密码时发生错误：{str(e)}")
    
    def delete_password(self, password_item: PasswordItem):
        """删除密码"""
        reply = NMessageBox.question(
            self,
            "确认删除",
            f"确定要删除密码{password_item.title}吗？\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )


        
        if reply == QMessageBox.Yes:
            if self.password_manager.delete_password(password_item.id):
                self.load_data()
                NMessageBox.information(self, "成功", "密码删除成功！")
            else:
                NMessageBox.critical(self, "错误", "删除失败！")
