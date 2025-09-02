from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QScrollArea, QWidget)
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from .base_page import BasePage


class HomePage(BasePage):
    """主页页面"""
    
    def __init__(self):
        super().__init__("主页")
    
    def init_ui(self):
        """初始化主页界面"""
        # 创建滚动区域
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
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        
        # 创建内容布局
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(6)
        content_layout.addWidget(self.create_intro_card())
        content_layout.addWidget(self.create_features_card())
        content_layout.addWidget(self.create_author_card())
        # 添加底部间距
        content_layout.addSpacing(6)
        # 设置滚动区域的内容
        scroll_area.setWidget(scroll_content)

        # 将滚动区域添加到主布局
        self.main_layout.addWidget(scroll_area)
    
    def create_title_card(self):
        """创建主标题卡片"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
                border: none;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        # 主标题
        title_label = QLabel("🔐 nuoqin管理平台")
        title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title_label.setStyleSheet("color: white; border: none;")
        title_label.setAlignment(Qt.AlignCenter)
        # 副标题
        subtitle_label = QLabel("安全、便捷的密码与书签管理工具")
        subtitle_label.setFont(QFont("Microsoft YaHei", 14))
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); border: none;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        return card
    
    def create_intro_card(self):
        """创建项目介绍卡片"""
        card = QFrame()
        card.setMinimumWidth(400)
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e1e8ed;
                padding: 15px;
                width: 400px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        # 标题
        title_label = QLabel("📖 项目介绍")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; ")
        # 介绍内容
        intro_text = """
        nuoqin管理平台是一个基于PyQt5开发的本地化管理工具，专注于为用户提供安全、便捷的数据管理体验。
🔹 采用AES加密技术，确保您的敏感数据安全无忧
🔹 支持密码管理，帮助您安全存储和管理各类账户信息
🔹 提供书签管理功能，让您的网络收藏井然有序
🔹 支持分类管理，让数据组织更加清晰高效
🔹 现代化的用户界面，操作简单直观
🔹 完全本地化存储，数据隐私完全由您掌控
        """
        intro_label = QLabel(intro_text.strip())
        intro_label.setFont(QFont("Microsoft YaHei", 11))
        intro_label.setStyleSheet("color: #34495e; border: none; line-height: 1.6;")
        intro_label.setWordWrap(True)
        intro_label.setAlignment(Qt.AlignLeft)
        
        layout.addWidget(title_label)
        layout.addWidget(intro_label)
        
        return card
    
    def create_features_card(self):
        """创建功能特性卡片"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e1e8ed;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        
        # 标题
        title_label = QLabel("✨ 核心功能")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; margin-bottom: 10px;")
        
        # 功能列表
        features_layout = QHBoxLayout()
        features_layout.setSpacing(6)
        
        # 密码管理功能
        password_feature = self.create_feature_item(
            "🔑",
            "密码管理",
            "安全存储账户密码\n支持分类和搜索\n一键复制密码"
        )
        
        # 书签管理功能
        bookmark_feature = self.create_feature_item(
            "🔖",
            "书签管理",
            "收藏网站链接\n分类整理书签\n快速访问收藏"
        )
        
        # 安全加密功能
        security_feature = self.create_feature_item(
            "🛡️",
            "安全加密",
            "AES加密存储\n自定义访问密码\n数据安全保障"
        )
        
        features_layout.addWidget(password_feature)
        features_layout.addWidget(bookmark_feature)
        features_layout.addWidget(security_feature)
        
        layout.addWidget(title_label)
        layout.addLayout(features_layout)
        
        return card
    
    def create_feature_item(self, icon, title, description):
        """创建功能项"""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(item)
        layout.setSpacing(6)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Microsoft YaHei", 24))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("border: none;")
        
        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; border: none;")
        
        # 描述
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Microsoft YaHei", 10))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #6c757d; border: none;")
        desc_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        return item
    
    def create_author_card(self):
        """创建作者信息卡片"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e1e8ed;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("👨‍💻 关于作者")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; margin-bottom: 10px;")
        
        # 作者信息布局
        author_layout = QHBoxLayout()
        author_layout.setSpacing(6)
        
        # 左侧：作者信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # 作者名称
        name_layout = QHBoxLayout()
        name_icon = QLabel("👤 作者：")
        name_icon.setFont(QFont("Microsoft YaHei", 12))
        name_icon.setStyleSheet("border: none;")
        name_label = QLabel("nuoqin")
        name_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50; border: none;")
        name_layout.addWidget(name_icon)
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        
        # GitHub地址
        github_layout = QHBoxLayout()
        github_icon = QLabel("🔗 GitHub：")
        github_icon.setFont(QFont("Microsoft YaHei", 12))
        github_icon.setStyleSheet("border: none;")
        github_label = QLabel("https://github.com/nuoqin")
        github_label.setFont(QFont("Microsoft YaHei", 12))
        github_label.setStyleSheet("color: #2c3e50; border: none;")
        github_layout.addWidget(github_icon)
        github_layout.addWidget(github_label)
        github_layout.addStretch()
        
        info_layout.addLayout(name_layout)
        info_layout.addLayout(github_layout)
        
        # 右侧：GitHub按钮
        button_layout = QVBoxLayout()
        github_btn = QPushButton("访问 GitHub")
        github_btn.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        github_btn.setStyleSheet("""
            QPushButton {
                background-color: #24292e;
                color: white;
                border: none;
                padding: 8px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0366d6;
            }
            QPushButton:pressed {
                background-color: #0256cc;
            }
        """)
        github_btn.clicked.connect(self.open_github)
        
        button_layout.addWidget(github_btn)
        button_layout.addStretch()
        
        author_layout.addLayout(info_layout, 2)
        author_layout.addLayout(button_layout, 1)
        
        # 感谢信息
        thanks_label = QLabel("感谢您使用nuoqin管理平台！如果您觉得这个项目有用，欢迎访问GitHub给个Star⭐")
        thanks_label.setFont(QFont("Microsoft YaHei", 10))
        thanks_label.setStyleSheet("color: #6c757d; border: none; padding: 10px; background-color: #f8f9fa; border-radius: 4px;")
        thanks_label.setWordWrap(True)
        thanks_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addLayout(author_layout)
        layout.addWidget(thanks_label)
        
        return card
    
    def open_github(self):
        """打开GitHub链接"""
        QDesktopServices.openUrl(QUrl("https://github.com/nuoqin/pd-bm"))
