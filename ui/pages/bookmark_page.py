"""书签管理页面模块"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QScrollArea, QWidget, QDialog, QTextEdit, 
    QFormLayout, QMessageBox, QGridLayout, QLayout, QSizePolicy, QApplication,
    QComboBox, QTabWidget, QColorDialog
)
from PyQt5.QtGui import QFont, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QTimer, QRect, QSize, QUrl

from utils.messagebox import NMessageBox
from .base_page import BasePage
from model import BookmarkManager, BookmarkItem, BookmarkCategoryManager


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


class BookmarkEditDialog(QDialog):
    """书签编辑对话框"""
    
    def __init__(self, parent=None, bookmark_item: BookmarkItem = None, category_manager=None):
        super().__init__(parent)
        self.bookmark_item = bookmark_item
        self.is_edit_mode = bookmark_item is not None
        self.category_manager = category_manager
        
        try:
            self.init_ui()
            
            # 如果是编辑模式，填充现有数据
            if self.is_edit_mode:
                self.load_data()
        except Exception as e:
            print(f"初始化书签编辑对话框时发生异常: {e}")
            import traceback
            traceback.print_exc()
    
    def init_ui(self):
        """初始化对话框UI"""
        self.setWindowTitle("编辑书签" if self.is_edit_mode else "添加书签")
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
            
            QComboBox {
                border-radius: 2px;
            }
            
            QComboBox:hover {
                border-color: #007acc;
            }
            
            QComboBox QAbstractItemView {
                border-radius: 2px;
                background-color: white;
                padding: 8px 0; 
                color: #333333;
                selection-background-color: #007acc;
                selection-color: white;
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
        self.title_edit.setPlaceholderText("请输入书签标题...")
        form_layout.addRow("标题 *:", self.title_edit)
        
        # 地址输入
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("请输入网址（如：https://www.example.com）...")
        form_layout.addRow("地址 *:", self.url_edit)
        
        # 分类选择
        self.category_combo = QComboBox()
        self.category_combo.setEditable(False)  # 允许输入新分类
        self.load_categories()
        form_layout.addRow("分类:", self.category_combo)
        
        # 描述输入（放到最后）
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("请输入描述...")
        self.description_edit.setMaximumHeight(80)
        form_layout.addRow("描述:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)  # 设置按钮间距
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        # 确认按钮
        confirm_btn = QPushButton("确认")
        confirm_btn.clicked.connect(self.accept_data)
        confirm_btn.setObjectName("confirmBtn")  # 设置对象名用于特定样式
        confirm_btn.setStyleSheet("""
            QPushButton#confirmBtn {
                background-color: #1890ff;
                border:none;
                color:white;
            }
            QPushButton#confirmBtn:hover {
                background-color: #007acc;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)
    
    def load_categories(self):
        """加载分类选项"""
        self.category_combo.clear()
        if self.category_manager:
            try:
                categories = self.category_manager.get_category_names()
                self.category_combo.addItems(categories)
            except:
                # 如果获取分类失败，添加默认分类
                self.category_combo.addItem("默认分类")
        else:
            self.category_combo.addItem("默认分类")
    
    def load_data(self):
        """加载现有数据"""
        try:
            self.title_edit.setText(self.bookmark_item.title)
            self.url_edit.setText(self.bookmark_item.url)
            self.description_edit.setPlainText(self.bookmark_item.description)
            
            # 设置分类
            category = getattr(self.bookmark_item, 'category', '默认分类')
            index = self.category_combo.findText(category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        except Exception as e:
            print(f"加载书签数据时发生异常: {e}")
            import traceback
            traceback.print_exc()
    
    def accept_data(self):
        """确认数据"""
        title = self.title_edit.text().strip()
        url = self.url_edit.text().strip()
        
        if not title or not url:
            NMessageBox.warning(self, "输入错误", "标题和地址不能为空！")
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """获取输入的数据"""
        return {
            'title': self.title_edit.text().strip(),
            'url': self.url_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'category': self.category_combo.currentText().strip() or "默认分类"
        }


class BookmarkCard(QFrame):
    """书签卡片组件"""
    
    def __init__(self, bookmark_item: BookmarkItem, parent=None):
        super().__init__(parent)
        self.bookmark_item = bookmark_item
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
        self.setFixedSize(300, 170)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(4)  # 设置组件间的默认间距
        
        # 标题标签 - 独占一行，确保完全显示
        title_label = QLabel(self.bookmark_item.title)
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setStyleSheet("color: black; border:none;")
        title_label.setMaximumHeight(26)  # 设置最小高度

        layout.addWidget(title_label)  # 添加标题标签
        
        # 分类信息行
        category_layout = QHBoxLayout()
        category_layout.setSpacing(8)
        category_layout.setContentsMargins(0, 4, 0, 4)
        
        category_label = QLabel("分类:")
        category_label.setFont(QFont("Microsoft YaHei", 10))
        category_label.setStyleSheet("color: #666666; border:none;")
        category_label.setFixedWidth(35)
        
        category_value = QLabel(getattr(self.bookmark_item, 'category', '默认分类'))
        category_value.setFont(QFont("Microsoft YaHei", 10))
        category_value.setStyleSheet("color: #28a745; border:none; font-weight: bold;")
        category_layout.addWidget(category_label)
        category_layout.addWidget(category_value, 1)
        layout.addLayout(category_layout)

        # 描述信息
        desc_layout = QHBoxLayout()
        desc_layout.setSpacing(8)
        desc_layout.setContentsMargins(0, 4, 0, 4)
        desc_label = QLabel("描述:")
        desc_label.setFont(QFont("Microsoft YaHei", 10))
        desc_label.setStyleSheet("color: #666666; border:none;")
        desc_label.setFixedWidth(35)
        desc_label.setAlignment(Qt.AlignTop)  # 顶部对齐
        desc_value = QLabel(getattr(self.bookmark_item, 'description', '无描述'))
        desc_value.setFont(QFont("Microsoft YaHei", 9))
        desc_value.setStyleSheet("color: #999999; border:none;")
        desc_value.setWordWrap(True)
        desc_value.setAlignment(Qt.AlignTop)
        desc_value.setMinimumHeight(36)
        desc_value.setMaximumHeight(36)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(desc_value, 1)
            
        layout.addLayout(desc_layout)
        # 添加弹性空间，将按钮推到底部
        layout.addStretch()
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(0, 8, 0, 0)
        
        # 访问按钮
        visit_btn = QPushButton("访问")
        visit_btn.setStyleSheet("""
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
        visit_btn.clicked.connect(self.visit_url)
        
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
        edit_btn.clicked.connect(self.edit_bookmark)
        
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
        delete_btn.clicked.connect(self.delete_bookmark)
        
        button_layout.addWidget(visit_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
    
    def visit_url(self):
        """访问网址"""
        url = self.bookmark_item.url
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            QDesktopServices.openUrl(QUrl(url))
        except Exception as e:
            NMessageBox.warning(self.parent_page, "打开失败", f"无法打开网址：{str(e)}")
    
    def edit_bookmark(self):
        """编辑书签"""
        if self.parent_page:
            self.parent_page.edit_bookmark(self.bookmark_item)
    
    def delete_bookmark(self):
        """删除书签"""
        if self.parent_page:
            self.parent_page.delete_bookmark(self.bookmark_item)


class BookmarkManagerPage(BasePage):
    """书签管理页面"""

    def __init__(self, encryption_key: str = None):
        super().__init__("书签管理")
        self.bookmark_manager = BookmarkManager()
        self.category_manager = BookmarkCategoryManager()
        self.current_bookmarks = []
        self.current_category = "全部"  # 当前选择的分类

        # 如果提供了加密密钥，设置加密模式
        if encryption_key:
            self.bookmark_manager.set_encryption_key(encryption_key)
            self.category_manager.set_encryption_key(encryption_key)

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
            }
            """
            
            # 合并样式表
            if "QMessageBox" not in current_style:
                app.setStyleSheet(current_style + messagebox_style)
    
    def init_ui(self):
        """初始化书签管理界面"""
        # 清除默认布局
        for i in reversed(range(self.main_layout.count())): 
            self.main_layout.itemAt(i).widget().setParent(None)
        # 功能区（上半部分）
        self.create_function_area()
        # 书签展示区（下半部分）
        self.create_bookmark_display_area()
    
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
        
        # 分类筛选下拉框
        self.category_filter = QComboBox()
        self.category_filter.setFixedHeight(34)
        self.category_filter.setFixedWidth(120)
        self.category_filter.setStyleSheet("""
            QComboBox {
                padding: 8px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 2px;
                font-size: 12px;
                background-color: #ffffff;
                color: #333333;
            }
            QComboBox:focus {
                border-color: #007acc;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        self.category_filter.currentTextChanged.connect(self.filter_by_category)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setPlaceholderText("搜索书签（标题、地址、描述、分类）...")
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
        self.search_edit.textChanged.connect(self.search_bookmarks)
        
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
        add_btn.clicked.connect(self.add_bookmark)
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
        
        layout.addWidget(self.category_filter)
        layout.addWidget(self.search_edit, 1)
        layout.addWidget(add_btn)
        layout.addWidget(refresh_btn)
        
        self.main_layout.addWidget(function_frame)
    
    def create_bookmark_display_area(self):
        """创建书签展示区"""
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
        """)
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        
        # 使用流式布局
        self.content_layout = FlowLayout(self.content_widget, margin=10, spacing=15)
        
        scroll_area.setWidget(self.content_widget)
        container_layout.addWidget(scroll_area)
        
        # 空状态提示标签
        self.empty_label = QLabel("暂无书签数据\n点击上方添加书签按钮开始添加", self.content_widget)
        self.empty_label.setFont(QFont("Microsoft YaHei", 14))
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setFixedSize(400, 150)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #999999;
                padding: 40px;
                border: 2px dashed #dddddd;
                border-radius: 8px;
                background-color: #fafafa;
            }
        """)
        self.empty_label.hide()
        
        # 无搜索结果提示标签
        self.no_results_label = QLabel("未找到匹配的书签\n请尝试其他关键词", self.content_widget)
        self.no_results_label.setFont(QFont("Microsoft YaHei", 14))
        self.no_results_label.setAlignment(Qt.AlignCenter)
        self.no_results_label.setFixedSize(350, 120)
        self.no_results_label.setStyleSheet("""
            QLabel {
                color: #999999;
                padding: 40px;
                border: none;
            }
        """)
        self.no_results_label.hide()
        
        self.main_layout.addWidget(display_container)
    
    def load_data(self):
        """加载所有数据"""
        try:
            # 加载分类数据
            self.category_manager.load_data()
            self.load_category_filter()
            
            # 加载书签数据
            self.bookmark_manager.load_data()
            self.filter_bookmarks()
        except Exception as e:
            if "访问密码错误" in str(e):
                # 显示密码错误提示，但不清空现有数据
                NMessageBox.critical(self, "访问密码错误",
                                     "无法解密数据！\n\n可能原因：\n"
                                     "1. 输入的访问密码与之前设置的不一致\n"
                                     "2. 加密文件已损坏\n\n"
                                     "请重新启动程序并输入正确的访问密码。")
                # 不更新显示，保持当前状态
                return
            else:
                # 其他错误，显示通用错误信息
                NMessageBox.critical(self, "加载失败", f"加载数据时发生错误：\n{str(e)}")
                self.current_bookmarks = []
                self.update_bookmark_display()
    
    def load_category_filter(self):
        """加载分类筛选选项"""
        self.category_filter.clear()
        self.category_filter.addItem("全部")
        
        try:
            categories = self.category_manager.get_category_names()
            self.category_filter.addItems(categories)
        except:
            # 如果获取分类失败，添加默认分类
            self.category_filter.addItem("默认分类")
    
    def filter_by_category(self, category_name):
        """根据分类筛选书签"""
        self.current_category = category_name
        self.filter_bookmarks()
    
    def filter_bookmarks(self):
        """筛选书签（结合分类和搜索）"""
        all_bookmarks = self.bookmark_manager.get_all_bookmarks()
        
        # 先按分类筛选
        if self.current_category == "全部":
            filtered_bookmarks = all_bookmarks
        else:
            filtered_bookmarks = [b for b in all_bookmarks if getattr(b, 'category', '默认分类') == self.current_category]
        
        # 再按搜索关键词筛选
        search_query = self.search_edit.text().strip()
        if search_query:
            search_query = search_query.lower()
            self.current_bookmarks = []
            for item in filtered_bookmarks:
                if (search_query in item.title.lower() or 
                    search_query in item.url.lower() or
                    search_query in item.description.lower() or
                    search_query in getattr(item, 'category', '默认分类').lower()):
                    self.current_bookmarks.append(item)
        else:
            self.current_bookmarks = filtered_bookmarks
        
        self.update_bookmark_display()
    
    def update_bookmark_display(self):
        """更新书签显示"""
        # 清除FlowLayout中的所有项目
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        # 获取搜索关键词
        search_query = self.search_edit.text().strip()
        total_bookmarks = len(self.bookmark_manager.get_all_bookmarks())
        
        # 更新搜索状态
        if search_query:
            # 显示搜索状态
            self.search_status_label.show()
            if self.current_bookmarks:
                self.search_status_label.setText(f"搜索 \"{search_query}\" 找到 {len(self.current_bookmarks)} 条记录")
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
        if not self.current_bookmarks:
            # 隐藏另一个提示标签
            self.empty_label.hide()
            self.no_results_label.hide()
            
            # 显示对应的提示标签
            if search_query:
                self.no_results_label.show()
                self.no_results_label.move(25, 25)
            elif total_bookmarks == 0:
                self.empty_label.show()
                self.empty_label.move(25, 25)
        else:
            # 隐藏提示标签
            self.empty_label.hide()
            self.no_results_label.hide()
            
            # 显示书签卡片（流式布局会自动换行）
            for i, bookmark_item in enumerate(self.current_bookmarks):
                card = BookmarkCard(bookmark_item, self)
                card.setProperty("cardIndex", i)
                self.content_layout.addWidget(card)
        
        # 更新布局
        self.content_widget.update()
    
    def search_bookmarks(self):
        """搜索书签"""
        self.filter_bookmarks()
    
    def add_bookmark(self):
        """添加书签"""
        dialog = BookmarkEditDialog(self, category_manager=self.category_manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.bookmark_manager.add_bookmark(
                title=data['title'],
                url=data['url'],
                description=data['description'],
                category=data['category']
            )
            self.load_data()
            NMessageBox.information(self, "成功", "书签添加成功！")
    
    def edit_bookmark(self, bookmark_item: BookmarkItem):
        """编辑书签"""
        try:
            dialog = BookmarkEditDialog(self, bookmark_item, self.category_manager)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                print(f"准备更新书签: {data['title']}")
                
                success = self.bookmark_manager.update_bookmark(
                    item_id=bookmark_item.id,
                    title=data['title'],
                    url=data['url'],
                    description=data['description'],
                    category=data['category']
                )
                
                if success:
                    print("书签更新成功，重新加载数据...")
                    self.load_data()
                    NMessageBox.information(self, "成功", "书签更新成功！")
                else:
                    print("书签更新失败")
                    NMessageBox.warning(self, "错误", "书签更新失败！")
        except Exception as e:
            print(f"编辑书签时发生异常: {e}")
            import traceback
            traceback.print_exc()
            NMessageBox.critical(self, "错误", f"编辑书签时发生错误：{str(e)}")
    
    def delete_bookmark(self, bookmark_item: BookmarkItem):
        """删除书签"""
        reply = NMessageBox.question(
            self,
            "确认删除",
            f"确定要删除书签{bookmark_item.title}吗？\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )


        
        if reply == QMessageBox.Yes:
            if self.bookmark_manager.delete_bookmark(bookmark_item.id):
                self.load_data()
                NMessageBox.information(self, "成功", "书签删除成功！")
            else:
                NMessageBox.critical(self, "错误", "删除失败！")
