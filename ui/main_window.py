"""主窗口模块"""
import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QStackedWidget, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt

from .pages import HomePage, PasswordManagerPage, BookmarkManagerPage, BookmarkCategoryManagerPage, SettingsPage, GenericPage
from utils.menu_utils import load_menu_config


class NavBar(QWidget):
    """主导航窗口类"""

    def __init__(self, encryption_key: str = None, theme_manager=None):
        super().__init__()

        # 保存加密密钥和主题管理器
        self.encryption_key = encryption_key
        self.theme_manager = theme_manager
        # 加载菜单配置
        self.config = load_menu_config()
        self.setWindowTitle("nuoqin管理器")
        self.resize(860, 500)
        self.setMinimumSize(860,500)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)  # 添加统一边距
        main_layout.setSpacing(12)  # 设置左右区域间距

        # 左侧导航栏容器
        nav_widget = QFrame()
        nav_width = self.config.get("config", {}).get("nav_width", 180)
        nav_widget.setFixedWidth(nav_width)
        nav_widget.setStyleSheet("background-color: white; color: black; border-radius: 12px;")
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setAlignment(Qt.AlignTop)
        nav_layout.setContentsMargins(12, 12, 12, 12)  # 导航栏内边距

        # 右侧堆叠窗口容器（添加统一样式）
        stack_container = QFrame()
        stack_container.setStyleSheet("background-color: white; color: black; border-radius: 12px;")
        stack_layout = QVBoxLayout(stack_container)
        stack_layout.setContentsMargins(12, 12, 12, 12)  # 右侧容器内边距
        
        # 右侧堆叠窗口（切换内容区域）
        self.stack = QStackedWidget()
        stack_layout.addWidget(self.stack)

        # 从配置文件读取菜单项并动态生成按钮
        self.buttons = []
        menu_items = self.config.get("menu_items", [])
        config_settings = self.config.get("config", {})
        
        # 获取配置参数
        button_height = config_settings.get("button_height", 45)
        font_family = config_settings.get("font_family", "Microsoft YaHei")
        font_size = config_settings.get("font_size", 10)
        
        # 创建普通菜单按钮（非设置类型）
        normal_items = [item for item in menu_items if item.get("type") != "settings"]
        
        for idx, item in enumerate(normal_items):
            text = item.get("text", "未命名")
            icon_path = item.get("icon", "")
            
            # 创建对应的页面
            page = self.create_page_by_name(text)
            
            # 创建按钮
            btn = QPushButton(text)
            if icon_path and os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))
            btn.setFixedHeight(button_height)
            btn.setFont(QFont(font_family, font_size))
            btn.setStyleSheet(self.get_btn_style(False))
            btn.setCursor(Qt.PointingHandCursor)

            nav_layout.addWidget(btn)
            self.buttons.append(btn)
            self.stack.addWidget(page)

            btn.clicked.connect(lambda _, i=idx: self.switch_page(i))

        # 中间加一个伸缩空白，把"设置"推到底部
        nav_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 设置按钮（单独处理，固定在底部）
        settings_items = [item for item in menu_items if item.get("type") == "settings"]
        
        for settings_item in settings_items:
            self.setting_index = len(self.buttons)
            text = settings_item.get("text", "设置")
            icon_path = settings_item.get("icon", "")
            
            setting_btn = QPushButton(text)
            if icon_path and os.path.exists(icon_path):
                setting_btn.setIcon(QIcon(icon_path))
            setting_btn.setIconSize(QSize(24, 24))
            setting_btn.setFixedHeight(button_height)
            setting_btn.setFont(QFont(font_family, font_size))
            setting_btn.setStyleSheet(self.get_btn_style(False))
            setting_btn.setCursor(Qt.PointingHandCursor)
            nav_layout.addWidget(setting_btn)

            self.buttons.append(setting_btn)
            self.stack.addWidget(self.create_page_by_name(text))

            setting_btn.clicked.connect(lambda _, i=self.setting_index: self.switch_page(i))

        # 默认选中第一个按钮
        self.switch_page(0)

        # 左侧导航 + 右侧堆叠页
        main_layout.addWidget(nav_widget, 0)  # 左侧固定宽度，不拉伸
        main_layout.addWidget(stack_container, 1)  # 右侧自适应剩余空间

    def get_btn_style(self, active=False):
        """按钮样式（圆角+高亮）"""
        if active:
            return """
                QPushButton {
                    background-color: #d6eaff;
                    border-radius: 2px;
                    text-align: left;
                    padding-left: 8px;
                    font-weight: bold;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 2px;
                    text-align: left;
                    padding-left: 12px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
            """

    def switch_page(self, index):
        """切换页面"""
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.setStyleSheet(self.get_btn_style(True))
            else:
                btn.setStyleSheet(self.get_btn_style(False))

    def create_page_by_name(self, page_name):
        """根据页面名称创建对应的页面实例"""
        if page_name.endswith("主页"):
            return HomePage()
        elif page_name.endswith("密码管理"):
            return PasswordManagerPage(encryption_key=self.encryption_key)
        elif page_name.endswith("书签管理"):
            return BookmarkManagerPage(encryption_key=self.encryption_key)
        elif page_name.endswith("书签分类"):
            return BookmarkCategoryManagerPage(encryption_key=self.encryption_key)
        elif page_name == "设置":
            settings_page = SettingsPage()
            # 连接主题切换信号
            if self.theme_manager:
                settings_page.theme_changed.connect(self.on_theme_changed)
            return settings_page
        else:
            return GenericPage(page_name)
    
    def on_theme_changed(self, theme_name):
        """处理主题切换"""
        if self.theme_manager:
            self.theme_manager.set_theme(theme_name)
            # 应用新主题样式
            from PyQt5.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                app.setStyleSheet(self.theme_manager.generate_main_window_style())


